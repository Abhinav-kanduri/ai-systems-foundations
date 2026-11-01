(function () {
  "use strict";
  const read = (key, fallback) => { try { return JSON.parse(localStorage.getItem(key)) || fallback; } catch (_) { return fallback; } };
  const write = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); } catch (_) {} };
  const themeButton = document.querySelector("#library-theme");
  let savedTheme;
  try { savedTheme = localStorage.getItem("fde-field-guide-theme"); } catch (_) {}
  document.documentElement.dataset.theme = savedTheme || "dark";
  themeButton?.addEventListener("click", () => {
    const theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem("fde-field-guide-theme", theme); } catch (_) {}
  });
  const menu = document.querySelector("#library-menu"), scrim = document.querySelector("#library-scrim");
  function closeMenu() { document.body.classList.remove("library-nav-open"); menu?.setAttribute("aria-expanded", "false"); menu?.setAttribute("aria-label", "Open library navigation"); if (scrim) scrim.hidden = true; document.querySelector('main').inert = false; }
  menu?.addEventListener("click", () => { const open = !document.body.classList.contains("library-nav-open"); document.body.classList.toggle("library-nav-open", open); menu.setAttribute("aria-expanded", String(open)); menu.setAttribute("aria-label", open ? "Close library navigation" : "Open library navigation"); scrim.hidden = !open; document.querySelector('main').inert = open; });
  scrim?.addEventListener("click", closeMenu);
  document.addEventListener("keydown", event => { if (event.key === "Escape") { closeMenu(); menu?.focus(); } });
  document.addEventListener('keydown',event=>{
    if(event.key!=='Tab'||menu?.getAttribute('aria-expanded')!=='true')return;
    const links=Array.from(document.querySelectorAll('#library-sidebar a'));
    if(event.shiftKey&&document.activeElement===menu){event.preventDefault();links.at(-1)?.focus();}
    else if(!event.shiftKey&&document.activeElement===links.at(-1)){event.preventDefault();menu.focus();}
  });
  const completion = document.querySelector("#complete-publication");
  const completionKey = "technical-publications-completed-v1";
  function updateCompletion() {
    if (!completion) return;
    const complete = Boolean(read(completionKey, {})[completion.dataset.publicationId]);
    completion.setAttribute("aria-pressed", String(complete));
    completion.textContent = complete ? "Marked as read ✓" : "Mark as read";
  }
  completion?.addEventListener("click", () => { const completed = read(completionKey, {}), id = completion.dataset.publicationId; if (completed[id]) delete completed[id]; else completed[id] = true; write(completionKey, completed); updateCompletion(); });
  updateCompletion();
  const body = document.querySelector("#publication-body"), progress = document.querySelector("#reading-progress");
  if (body && progress) {
    let scheduled = false;
    const headings = Array.from(body.querySelectorAll("h2[id], h3[id], h4[id]"));
    function updateReading() {
      scheduled = false;
      const start = body.getBoundingClientRect().top + window.scrollY - 110;
      const length = Math.max(1, body.offsetHeight - window.innerHeight + 180);
      const percent = Math.round(Math.min(1, Math.max(0, (window.scrollY - start) / length)) * 100);
      progress.setAttribute("aria-valuenow", String(percent)); progress.querySelector("span").style.width = percent + "%";
      const active = headings.filter(h => h.getBoundingClientRect().top <= 150).at(-1) || headings[0];
      document.querySelectorAll("[data-toc]").forEach(link => { if (link.dataset.toc === active?.id) link.setAttribute("aria-current", "location"); else link.removeAttribute("aria-current"); });
    }
    window.addEventListener("scroll", () => { if (!scheduled) { scheduled = true; requestAnimationFrame(updateReading); } }, {passive:true});
    window.addEventListener("resize", updateReading); updateReading();
  }
  const form = document.querySelector("#publication-filters");
  if (form) {
    const results = document.querySelector("#publication-results"), count = document.querySelector("#results-count");
    const fields = ["q", "topic", "type", "difficulty", "year", "reading", "series", "sort"];
    const escape = value => String(value || "").replace(/[&<>"']/g, c => ({"&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"}[c]));
    const siteRoot = new URL(document.body.dataset.siteRoot, location.href);
    let library;
    function card(p) {
      const category = library.taxonomy.categories.find(c => c.id === p.primaryCategory);
      const type = library.taxonomy.publicationTypes.find(t => t.id === p.publicationType);
      const link = new URL(p.reader === "fde" ? "#end-to-end-fde-learning-map" : "publications/" + p.slug + "/", siteRoot).href;
      const published = new Intl.DateTimeFormat("en", {year:"numeric", month:"short", day:"numeric", timeZone:"UTC"}).format(new Date(p.publishedAt));
      return `<article class="publication-card" data-publication-id="${escape(p.id)}"><div class="card-kicker"><span class="type-badge">${escape(type?.title)}</span><span>${escape(published)}</span></div><h3><a href="${escape(link)}">${escape(p.title)}</a></h3><p>${escape(p.summary)}</p><div class="publication-card-bottom"><span>${escape(category?.title)}</span><span>${p.readingTime} min read</span>${p.difficulty ? `<span>${escape(p.difficulty)}</span>` : ""}</div><a class="text-action" href="${escape(link)}">Read publication <span aria-hidden="true">↗</span><span class="sr-only">: ${escape(p.title)}</span></a></article>`;
    }
    const defaults = Object.fromEntries(fields.map(name => [name, form.elements[name].value]));
    function readUrl() {
      const params = new URLSearchParams(location.search);
      fields.forEach(name => { form.elements[name].value = params.has(name) ? params.get(name) : defaults[name]; });
    }
    function apply(updateUrl = true) {
      if (!library) return;
      const filters = Object.fromEntries(fields.map(name => [name, form.elements[name].value]));
      if (form.dataset.collectionIds) filters.collectionIds = JSON.parse(form.dataset.collectionIds);
      const matches = window.PublicationSearch.select(library.publications, filters, library.taxonomy, library.collections);
      count.textContent = matches.length + (matches.length === 1 ? " publication" : " publications");
      results.innerHTML = matches.length ? matches.map(card).join("") : '<div class="library-empty"><strong>No publications match your search.</strong><p>Try another phrase or clear the filters to explore more of the library.</p></div>';
      if (updateUrl) {
        const url = new URL(location.href);
        fields.forEach(name => { const value = filters[name]; if (value && (name !== "sort" || value !== "latest")) url.searchParams.set(name, value); else url.searchParams.delete(name); });
        history.replaceState(null, "", url);
      }
    }
    form.addEventListener("submit", event => { event.preventDefault(); apply(); });
    form.addEventListener("input", () => apply());
    form.addEventListener("change", () => apply());
    document.querySelector("#clear-filters").addEventListener("click", () => { form.reset(); form.elements.q.value = ""; apply(); form.elements.q.focus(); });
    window.addEventListener("popstate", () => { readUrl(); apply(false); });
    fetch(document.body.dataset.manifest).then(response => { if (!response.ok) throw new Error("Library index unavailable"); return response.json(); }).then(data => { library = data; readUrl(); apply(false); }).catch(() => { count.textContent = "Search is unavailable. Refresh to try again."; });
  }
  document.querySelectorAll("[data-collection-members]").forEach(element => {
    const completed = read(completionKey, {}), curriculum = new Set(read("fde-field-guide-progress-v1", []));
    const members = JSON.parse(element.dataset.collectionMembers);
    const total = members.filter(p => p.reader === "fde" ? p.chapterSlugs.every(slug => curriculum.has(slug)) : Boolean(completed[p.id])).length;
    element.textContent = total + " of " + members.length + " publications completed";
  });
})();
