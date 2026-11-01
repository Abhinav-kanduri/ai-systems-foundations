(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.PublicationSearch = api;
})(typeof globalThis === "object" ? globalThis : this, function () {
  "use strict";
  const normalize = value => String(value || "").normalize("NFKC").toLocaleLowerCase("en");
  const date = value => Date.parse(value || "") || 0;
  function select(publications, filters = {}, taxonomy = {}, collections = {}) {
    const categories = new Map((taxonomy.categories || []).map(c => [c.id, c.title]));
    const parents = new Map((taxonomy.categories || []).map(c => [c.id, c.parentId]));
    const memberships = p => { const ids = new Set(); for (let id of [p.primaryCategory, ...(p.secondaryCategories || [])]) { while(id && !ids.has(id)){ids.add(id);id=parents.get(id);} } return Array.from(ids); };
    const terms = normalize(filters.q).trim().split(/\s+/).filter(Boolean);
    const series = (collections.series || []).find(c => c.id === filters.series);
    const order = filters.collectionIds || series?.publicationIds || [];
    const ranked = publications.filter(p => {
      if (filters.topic && !memberships(p).includes(filters.topic)) return false;
      if (filters.type && p.publicationType !== filters.type) return false;
      if (filters.difficulty && p.difficulty !== filters.difficulty) return false;
      if (filters.year && String(p.publishedAt).slice(0, 4) !== filters.year) return false;
      if (filters.series && !series?.publicationIds.includes(p.id)) return false;
      if (filters.collectionIds && !filters.collectionIds.includes(p.id)) return false;
      if (filters.reading === "short" && p.readingTime >= 10) return false;
      if (filters.reading === "medium" && (p.readingTime < 10 || p.readingTime > 30)) return false;
      if (filters.reading === "long" && p.readingTime <= 30) return false;
      return true;
    }).map(p => {
      const collectionTitle = (collections.series || []).filter(c => c.publicationIds.includes(p.id)).map(c => c.title).join(' ');
      const groups = [[p.title, 12], [p.subtitle, 6], [p.summary, 5], [p.researchOrganization, 7], [collectionTitle, 6], [(p.tags || []).join(" "), 7], [(p.technologies || []).join(" "), 6], [memberships(p).map(c => categories.get(c) || c).join(" "), 5], [p.searchText, 1]];
      let score = 0;
      for (const term of terms) {
        const rank = groups.reduce((total, [text, weight]) => total + (normalize(text).includes(term) ? weight : 0), 0);
        if (!rank) return null;
        score += rank;
      }
      return {p, score};
    }).filter(Boolean);
    ranked.sort((a, b) => {
      if (terms.length && (!filters.sort || filters.sort === "relevance") && a.score !== b.score) return b.score - a.score;
      const first = a.p, second = b.p;
      let comparison;
      switch (filters.sort) {
        case "oldest": comparison = date(first.publishedAt) - date(second.publishedAt); break;
        case "updated": comparison = date(second.updatedAt || second.publishedAt) - date(first.updatedAt || first.publishedAt); break;
        case "title": comparison = first.title.localeCompare(second.title, "en"); break;
        case "recommended": {
          const rank = id => order.includes(id) ? order.indexOf(id) : Number.MAX_SAFE_INTEGER;
          comparison = rank(first.id) - rank(second.id); break;
        }
        default: comparison = date(second.publishedAt) - date(first.publishedAt);
      }
      return comparison || first.id.localeCompare(second.id, "en");
    });
    return ranked.map(value => value.p);
  }
  return {select};
});
