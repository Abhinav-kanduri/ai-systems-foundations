(function () {
  "use strict";

  const CONTENT_PATHS = ["content/fde-learning-map.md", "../FordwardDeployementEngineer.md"];
  const STORAGE_KEY = "fde-field-guide-progress-v1";

  const groups = [
    { label: "Orientation", match: (number, slug) => !number && slug === "end-to-end-fde-learning-map" },
    { label: "Discover & plan", match: (number) => number >= 1 && number <= 3 },
    { label: "Build foundations", match: (number) => number >= 4 && number <= 9 },
    { label: "Ship enterprise systems", match: (number) => number >= 10 && number <= 13 },
    { label: "Engineer applied AI", match: (number) => number >= 14 && number <= 19 },
    { label: "Operate & scale", match: (number) => number >= 20 && number <= 23 },
    { label: "Lead & land", match: (number) => number >= 24 && number <= 27 },
    { label: "Your roadmap", match: (number, slug) => !number && slug !== "end-to-end-fde-learning-map" },
  ];

  const state = {
    sections: [],
    references: {},
    completed: new Set(readProgress()),
    activeSlug: "",
  };

  const elements = {
    content: document.querySelector("#chapter-content"),
    nav: document.querySelector("#chapter-nav"),
    search: document.querySelector("#chapter-search"),
    progressCount: document.querySelector("#progress-count"),
    progressTotal: document.querySelector("#progress-total"),
    progressBar: document.querySelector("#progress-bar"),
    position: document.querySelector("#chapter-position"),
    completeButton: document.querySelector("#complete-button"),
    completeLabel: document.querySelector(".complete-label"),
    previous: document.querySelector("#previous-chapter"),
    next: document.querySelector("#next-chapter"),
    overview: document.querySelector("#overview-dashboard"),
    theme: document.querySelector(".theme-toggle"),
    menu: document.querySelector(".menu-toggle"),
    scrim: document.querySelector(".sidebar-scrim"),
  };

  function slugify(value) {
    return value
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, "")
      .trim()
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-");
  }

  function escapeHtml(value) {
    const node = document.createElement("div");
    node.textContent = value;
    return node.innerHTML;
  }

  function renderInline(value) {
    let html = escapeHtml(value);
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\[([^\]]+)\]\[(\d+)\]/g, function (_, label, id) {
      const reference = state.references[id];
      return reference
        ? `<a href="${escapeHtml(reference.url)}" target="_blank" rel="noreferrer">${label}</a>`
        : label;
    });
    html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
    return html;
  }

  function parseMarkdown(markdown) {
    const referencePattern = /^\[(\d+)\]:\s+(\S+)(?:\s+"([^"]+)")?\s*$/gm;
    markdown = markdown.replace(referencePattern, function (_, id, url, title) {
      state.references[id] = { url, title: title || "" };
      return "";
    });

    const lines = markdown.replace(/\r/g, "").split("\n");
    const sections = [];
    let current = null;

    lines.forEach(function (line) {
      const heading = line.match(/^#\s+(.+)$/);
      if (heading) {
        if (current) sections.push(current);
        const title = heading[1].trim();
        const numberMatch = title.match(/^(\d+)\.\s+/);
        current = {
          title,
          number: numberMatch ? Number(numberMatch[1]) : null,
          slug: slugify(title),
          body: [],
        };
      } else if (current) {
        current.body.push(line);
      }
    });

    if (current) sections.push(current);
    return sections;
  }

  function markdownToHtml(lines) {
    let html = "";
    let listType = "";

    function closeList() {
      if (listType) html += `</${listType}>`;
      listType = "";
    }

    lines.forEach(function (line) {
      const h2 = line.match(/^##\s+(.+)$/);
      const h3 = line.match(/^###\s+(.+)$/);
      const bullet = line.match(/^\*\s+(.+)$/);
      const ordered = line.match(/^\d+\.\s+(.+)$/);
      const quote = line.match(/^>\s*(.+)$/);

      if (bullet || ordered) {
        const nextType = bullet ? "ul" : "ol";
        if (listType !== nextType) {
          closeList();
          listType = nextType;
          html += `<${listType}>`;
        }
        html += `<li>${renderInline((bullet || ordered)[1])}</li>`;
        return;
      }

      closeList();
      if (h3) html += `<h3>${renderInline(h3[1])}</h3>`;
      else if (h2) html += `<h2>${renderInline(h2[1])}</h2>`;
      else if (quote) html += `<blockquote><p>${renderInline(quote[1])}</p></blockquote>`;
      else if (/^---+$/.test(line.trim())) html += "<hr />";
      else if (line.trim()) html += `<p>${renderInline(line.trim())}</p>`;
    });

    closeList();
    return html;
  }

  function navLabel(section) {
    return section.number ? section.title.replace(/^\d+\.\s*/, "") : section.title;
  }

  function renderNavigation(query) {
    const normalizedQuery = (query || "").trim().toLowerCase();
    const matches = state.sections.filter(function (section) {
      return !normalizedQuery || `${section.title} ${section.body.join(" ")}`.toLowerCase().includes(normalizedQuery);
    });

    if (!matches.length) {
      elements.nav.innerHTML = '<div class="nav-empty">No chapters match that search.<br />Try a broader term.</div>';
      return;
    }

    elements.nav.innerHTML = groups.map(function (group) {
      const items = matches.filter((section) => group.match(section.number, section.slug));
      if (!items.length) return "";
      return `
        <section class="nav-group">
          <h2 class="nav-group-title">${group.label}</h2>
          ${items.map(function (section) {
            const index = section.number ? String(section.number).padStart(2, "0") : section.slug === "end-to-end-fde-learning-map" ? "00" : "↳";
            const completed = state.completed.has(section.slug) ? " completed" : "";
            const active = section.slug === state.activeSlug ? " active" : "";
            return `
              <a class="nav-link${completed}${active}" href="#${section.slug}" data-slug="${section.slug}">
                <span class="nav-index">${index}</span>
                <span>${escapeHtml(navLabel(section))}</span>
                <span class="nav-check" aria-label="Completed">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 12 3.2 3.2L17.5 8" /></svg>
                </span>
              </a>`;
          }).join("")}
        </section>`;
    }).join("");
  }

  function renderSection(section, shouldFocus) {
    const index = state.sections.indexOf(section);
    const isOverview = section.slug === "end-to-end-fde-learning-map";
    state.activeSlug = section.slug;

    document.title = `${navLabel(section)} · FDE Field Guide`;
    elements.overview.hidden = !isOverview;
    elements.position.textContent = section.number
      ? `Chapter ${String(section.number).padStart(2, "0")} of 27`
      : isOverview ? "Orientation" : "Personal roadmap";

    const titleHtml = section.number
      ? `<span class="chapter-number">CHAPTER ${String(section.number).padStart(2, "0")}</span>${escapeHtml(navLabel(section))}`
      : escapeHtml(isOverview ? "The FDE operating model" : section.title);
    elements.content.innerHTML = `<h1>${titleHtml}</h1>${markdownToHtml(section.body)}`;

    const trackable = Boolean(section.number);
    elements.completeButton.hidden = !trackable;
    if (trackable) updateCompleteButton(section.slug);

    updatePagination(index);
    renderNavigation(elements.search.value);
    closeMenu();
    window.scrollTo({ top: 0, behavior: shouldFocus ? "smooth" : "auto" });
    if (shouldFocus) elements.content.focus({ preventScroll: true });
  }

  function updatePagination(index) {
    const previous = state.sections[index - 1];
    const next = state.sections[index + 1];
    setPaginationLink(elements.previous, previous);
    setPaginationLink(elements.next, next);
  }

  function setPaginationLink(element, section) {
    element.hidden = !section;
    if (!section) return;
    element.href = `#${section.slug}`;
    element.querySelector("span").textContent = navLabel(section);
  }

  function updateCompleteButton(slug) {
    const complete = state.completed.has(slug);
    elements.completeButton.classList.toggle("is-complete", complete);
    elements.completeButton.setAttribute("aria-pressed", String(complete));
    elements.completeLabel.textContent = complete ? "Chapter completed" : "Mark chapter complete";
  }

  function toggleComplete() {
    const section = state.sections.find((item) => item.slug === state.activeSlug);
    if (!section || !section.number) return;
    if (state.completed.has(section.slug)) state.completed.delete(section.slug);
    else state.completed.add(section.slug);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(state.completed)));
    updateCompleteButton(section.slug);
    updateProgress();
    renderNavigation(elements.search.value);
  }

  function updateProgress() {
    const courseSlugs = new Set(state.sections.filter((section) => section.number).map((section) => section.slug));
    const completedCount = Array.from(state.completed).filter((slug) => courseSlugs.has(slug)).length;
    const total = courseSlugs.size || 27;
    elements.progressCount.textContent = completedCount;
    elements.progressTotal.textContent = total;
    elements.progressBar.style.width = `${Math.round((completedCount / total) * 100)}%`;
  }

  function readProgress() {
    try {
      const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      return Array.isArray(value) ? value : [];
    } catch (_) {
      return [];
    }
  }

  function route(shouldFocus) {
    if (!state.sections.length) return;
    const requested = decodeURIComponent(window.location.hash.slice(1));
    const section = state.sections.find((item) => item.slug === requested) || state.sections[0];
    if (!requested) history.replaceState(null, "", `#${section.slug}`);
    renderSection(section, shouldFocus);
  }

  function openMenu() {
    document.body.classList.add("nav-open");
    elements.menu.setAttribute("aria-expanded", "true");
    elements.menu.setAttribute("aria-label", "Close course navigation");
  }

  function closeMenu() {
    document.body.classList.remove("nav-open");
    elements.menu.setAttribute("aria-expanded", "false");
    elements.menu.setAttribute("aria-label", "Open course navigation");
  }

  function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("fde-field-guide-theme", theme);
  }

  async function loadMarkdown() {
    let lastError;
    for (const path of CONTENT_PATHS) {
      try {
        const response = await fetch(path);
        if (!response.ok) throw new Error(`Request failed: ${response.status}`);
        return await response.text();
      } catch (error) {
        lastError = error;
      }
    }
    throw lastError || new Error("The guide could not be loaded.");
  }

  async function initialize() {
    const savedTheme = localStorage.getItem("fde-field-guide-theme");
    const preferredTheme = window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
    setTheme(savedTheme || preferredTheme);

    try {
      const markdown = await loadMarkdown();
      state.sections = parseMarkdown(markdown);
      updateProgress();
      route(false);
    } catch (error) {
      elements.content.innerHTML = `
        <div class="error-state">
          <h1>Guide unavailable</h1>
          <p>The learning map could not be loaded. Serve this folder over HTTP or run the GitHub Pages workflow.</p>
        </div>`;
      console.error(error);
    }
  }

  window.addEventListener("hashchange", () => route(true));
  elements.search.addEventListener("input", (event) => renderNavigation(event.target.value));
  elements.completeButton.addEventListener("click", toggleComplete);
  elements.theme.addEventListener("click", function () {
    setTheme(document.documentElement.dataset.theme === "light" ? "dark" : "light");
  });
  elements.menu.addEventListener("click", function () {
    document.body.classList.contains("nav-open") ? closeMenu() : openMenu();
  });
  elements.scrim.addEventListener("click", closeMenu);
  document.addEventListener("keydown", function (event) {
    if (event.key === "/" && document.activeElement !== elements.search) {
      event.preventDefault();
      elements.search.focus();
    }
    if (event.key === "Escape") {
      elements.search.blur();
      closeMenu();
    }
  });

  initialize();
})();
