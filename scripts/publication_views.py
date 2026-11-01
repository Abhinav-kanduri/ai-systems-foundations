"""Static presentation components sharing the original FDE design tokens."""
from __future__ import annotations

import html
import json
import posixpath
from urllib.parse import urlsplit

from publication_model import category_memberships, parse_date


def esc(value):
    return html.escape(str(value or ""), quote=True)


def root_link(route, target=""):
    depth = len([p for p in route.strip("/").split("/") if p])
    return "../" * depth + target


def author_banner(library, route, lazy=False):
    banner=library['site'].get('authorBanner')
    if not banner:
        return ''
    source=root_link(route,banner['src'])
    return f'<figure class="author-banner"><img src="{esc(source)}" alt="{esc(banner["alt"])}" width="{int(banner["width"])}" height="{int(banner["height"])}" loading="{"lazy" if lazy else "eager"}" decoding="async"></figure>'


def editorial_note(library, route=''):
    note=library['site'].get('editorialNote')
    if not note:
        return ''
    links = []
    for link in note.get('links', []):
        if urlsplit(link['url']).scheme in {'https', 'http'}:
            links.append(f'<a href="{esc(link["url"])}" target="_blank" rel="noopener noreferrer">{esc(link["label"])} <span aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a>')
    invitation = f'<p class="editorial-invitation">{esc(note["invitation"])}</p>' if note.get('invitation') else ''
    about = f'<a href="{root_link(route,"publications/about/")}">About this learning library <span aria-hidden="true">→</span></a>'
    return f'<section class="editorial-note" id="about-publications" aria-labelledby="editorial-note-title"><h2 id="editorial-note-title">{esc(note["title"])}</h2><p>{esc(note["body"])}</p>{invitation}<nav class="editorial-links" aria-label="Explore our learning community">{about}{"".join(links)}</nav><p class="editorial-attribution"><em>{esc(note.get("attribution"))}</em></p></section>'


def publication_link(route, publication):
    return root_link(route, "#end-to-end-fde-learning-map" if publication.get("reader") == "fde" else f"publications/{publication['slug']}/")


def date_label(value):
    if not value:
        return ""
    return parse_date(value).strftime("%b %d, %Y").replace(" 0", " ")


def card(publication, library, route):
    category = next(c for c in library["taxonomy"]["categories"] if c["id"] == publication["primaryCategory"])
    type_name = next(t["title"] for t in library["taxonomy"]["publicationTypes"] if t["id"] == publication["publicationType"])
    difficulty = f'<span>{esc(publication["difficulty"].title())}</span>' if publication.get("difficulty") else ""
    return f'''<article class="publication-card" data-publication-id="{esc(publication['id'])}">
      <div class="card-kicker"><span class="type-badge">{esc(type_name)}</span><span>{esc(date_label(publication.get('publishedAt')))}</span></div>
      <h3><a href="{esc(publication_link(route, publication))}">{esc(publication['title'])}</a></h3>
      <p>{esc(publication['summary'])}</p>
      <div class="publication-card-bottom"><span>{esc(category['title'])}</span><span>{publication['readingTime']} min read</span>{difficulty}</div>
      <a class="text-action" href="{esc(publication_link(route, publication))}">Read publication <span aria-hidden="true">↗</span><span class="sr-only">: {esc(publication['title'])}</span></a>
    </article>'''


def cards(publications, library, route):
    if not publications:
        return '<div class="library-empty"><strong>There’s more to explore ahead.</strong><p>No publications in this collection yet. Browse the library or try another topic.</p></div>'
    return ''.join(card(p, library, route) for p in publications)


def collection_cards(kind, library, route):
    values = library['collections'][kind]
    if not values:
        return '<div class="library-empty"><strong>A space for connected ideas.</strong><p>Collections will appear here as publications are connected into a reading sequence.</p></div>'
    return ''.join(f'''<a class="collection-card" href="{root_link(route, f"publications/{kind}/{esc(c['slug'])}/")}"><span class="micro-label">{'READING SERIES' if kind == 'series' else 'LEARNING PATH'}</span><h3>{esc(c['title'])} <span aria-hidden="true">↗</span></h3><p>{esc(c['description'])}</p><small>{len(c['publicationIds'])} publication{'s' if len(c['publicationIds']) != 1 else ''} · {c['readingTime']} min</small></a>''' for c in values)


def shell(library, route, title, description, body, active='overview', article=None):
    site = library['site']
    href = lambda target='': root_link(route, target)
    canonical = article.get('canonicalUrl') if article else site['siteUrl'] + route
    nav = [('overview', 'Overview', 'publications/'), ('latest', 'Latest publications', 'publications/latest/'), ('topics', 'Explore topics', 'publications/topics/'), ('series', 'Publication series', 'publications/series/'), ('paths', 'Learning paths', 'publications/paths/'), ('about', 'About the library', 'publications/about/')]
    navigation = ''.join(f'<a href="{href(target)}" {"aria-current=page" if key == active else ""}><span class="nav-index">{index:02}</span>{label}</a>' for index, (key, label, target) in enumerate(nav))
    featured = ''.join(f'<a href="{href("publications/series/" + c["slug"] + "/")}"><span class="collection-dot" aria-hidden="true"></span>{esc(c["title"])}</a>' for c in library['collections']['series'])
    featured_nav = f'<h2 class="micro-label">FEATURED COLLECTIONS</h2>{featured}' if featured else ''
    title_full = title + ' · ' + site['title']
    structured = {'@context':'https://schema.org','@type':'Article' if article else 'CollectionPage','headline':title,'description':description,'url':canonical}
    if article:
        if article.get('author'):
            structured['author']={'@type':'Person','name':article['author']}
        for source,target in [('publishedAt','datePublished'),('updatedAt','dateModified')]:
            if article.get(source):
                structured[target]=article[source]
    structured_json=json.dumps(structured,ensure_ascii=False).replace('<','\\u003c')
    reader_script = f'<script src="{href("assets/research-reader.js")}" defer></script>' if article and article.get('problemNumber') else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#080d19">
<title>{esc(title_full)}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(canonical)}"><meta property="og:image" content="{esc(site['siteUrl'])}assets/publications-social.png"><meta name="twitter:card" content="summary_large_image"><script type="application/ld+json">{structured_json}</script>
<link rel="alternate" type="application/rss+xml" title="Technical Publications" href="{href('publications/feed.xml')}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{href('assets/styles.css')}"><link rel="stylesheet" href="{href('assets/publications.css')}"><link rel="stylesheet" href="{href('assets/resources.css')}"><link rel="stylesheet" href="{href('assets/code.css')}"><script src="{href('assets/publication-search.js')}" defer></script><script src="{href('assets/publications.js')}" defer></script>
<link rel="stylesheet" href="{href('assets/research.css')}">{reader_script}
</head><body class="publication-site" data-site-root="{href()}" data-manifest="{href('publications/index.json')}">
<a class="skip-link" href="#main-content">Skip to content</a>
<header class="library-topbar"><a class="library-brand" href="{href('publications/')}"><span class="library-brand-mark" aria-hidden="true">↗</span><span>ENGINEERING<span class="brand-subtitle">TECHNICAL PUBLICATIONS</span></span></a><span class="library-header-note"><span class="status-dot"></span> Ideas built for the real world</span><div class="library-top-actions"><a href="{href('#end-to-end-fde-learning-map')}" class="guide-link">FDE Field Guide <span aria-hidden="true">↗</span></a><button class="icon-button" id="library-theme" type="button" aria-label="Switch color theme">◐</button><button class="icon-button library-menu" id="library-menu" type="button" aria-label="Open library navigation" aria-expanded="false" aria-controls="library-sidebar">☰</button></div></header>
<aside class="library-sidebar" id="library-sidebar" aria-label="Technical Publications navigation"><div class="sidebar-intro"><span class="micro-label">THE KNOWLEDGE LIBRARY</span><p>Explore ideas.<br>Build understanding.</p></div><nav aria-label="Publications">{navigation}</nav><div class="featured-nav">{featured_nav}</div><div class="library-sidebar-bottom"><span class="micro-label">WRITTEN BY</span><strong>{esc(site.get('defaultAuthor'))}</strong><a href="{esc(site['repositoryUrl'])}" target="_blank" rel="noreferrer">Explore the repository <span aria-hidden="true">↗</span></a></div></aside>
<button class="library-scrim" id="library-scrim" aria-label="Close navigation" hidden></button>
<main class="library-main" id="main-content" tabindex="-1">{body}{editorial_note(library,route)}<footer class="library-footer"><span>Technical Publications</span><span>Engineering knowledge, from concept to production.</span><a href="{href('publications/feed.xml')}">RSS feed ↗</a></footer></main></body></html>'''


def about_page(library, rendered):
    title = 'Technical knowledge, made accessible to everyone.'
    intro = '<header class="library-page-heading"><span class="micro-label">ABOUT THE LIBRARY · OUR LEARNING PHILOSOPHY</span><h1>' + esc(title) + '</h1></header>'
    content = __import__('re').sub(r'<h1\b[^>]*>.*?</h1>', '', rendered, count=1, flags=__import__('re').S)
    body = intro + '<article class="publication-prose learning-philosophy">' + content + '</article>'
    return shell(library, 'publications/about/', title, 'An independent learning space for curious minds, students, aspiring engineers, and professionals.', body, active='about')


def controls(library, selected_topic='', selected_series=''):
    def options(values, key, label, selected=''):
        return ''.join(f'<option value="{esc(v[key])}" {"selected" if v[key] == selected else ""}>{esc(v[label])}</option>' for v in values)
    return f'''<form class="library-filters" id="publication-filters" role="search"><div class="publication-search-wrap"><label for="publication-query">Search the library</label><input id="publication-query" name="q" type="search" placeholder="Search ideas, technologies, or a phrase…" autocomplete="off"></div><div class="filter-grid">
<label>Technical domain<select name="topic"><option value="">All domains</option>{options(library['taxonomy']['categories'],'id','title',selected_topic)}</select></label>
<label>Publication type<select name="type"><option value="">All types</option>{options(library['taxonomy']['publicationTypes'],'id','title')}</select></label>
<label>Difficulty<select name="difficulty"><option value="">All levels</option><option value="beginner">Beginner</option><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option></select></label>
<label>Year<select name="year"><option value="">All years</option>{''.join(f'<option>{year}</option>' for year in sorted({p['publishedAt'][:4] for p in library['publications']},reverse=True))}</select></label>
<label>Reading time<select name="reading"><option value="">Any length</option><option value="short">Under 10 min</option><option value="medium">10–30 min</option><option value="long">Over 30 min</option></select></label>
<label>Series<select name="series"><option value="">All series</option>{options(library['collections']['series'],'id','title',selected_series)}</select></label>
<label>Sort by<select name="sort"><option value="latest">Newest first</option><option value="relevance">Most relevant</option><option value="oldest">Oldest first</option><option value="updated">Recently updated</option><option value="title">Alphabetical</option><option value="recommended">Recommended order</option></select></label><button type="button" id="clear-filters" class="secondary-action">Clear filters</button></div></form>'''


def topic_tiles(library, route):
    output = []
    categories={c['id']:c for c in library['taxonomy']['categories']}
    for index, c in enumerate(library['taxonomy']['categories']):
        count = sum(c['id'] in category_memberships(p,categories) for p in library['publications'])
        output.append(f'''<a class="domain-tile" href="{root_link(route, 'publications/topics/' + c['slug'] + '/')}"><span class="domain-number">{index+1:02}</span><div><h3>{esc(c['title'])}</h3><p>{esc(c.get('description'))}</p></div><span class="domain-count">{count}<span class="sr-only"> publications</span></span></a>''')
    return ''.join(output)


def index_page(library, route='publications/', kind='overview', category=None, collection=None):
    publications = library['publications']
    header, sections = '', ''
    title, description = 'Technical Publications', library['site']['description']
    if kind == 'overview':
        count = len(publications)
        header = f'''<section class="library-hero"><div class="eyebrow"><span></span> TECHNICAL PUBLICATIONS & RESEARCH</div><div class="library-hero-grid"><div><h1>Explore.<br>Engineer.<br><em>Discover.</em></h1><p>{esc(library["site"].get("heroSubtitle",library["site"]["description"]))}</p><a class="primary-action" href="#all-publications">Explore the library <span aria-hidden="true">↗</span></a></div><div class="hero-index"><span class="micro-label">A CONTINUOUSLY GROWING REFERENCE</span><div class="hero-index-number">{count:02}<span>publication{'s' if count != 1 else ''}</span></div><div class="hero-index-line"><span>Concept → implementation</span><span aria-hidden="true">↗</span></div><div class="hero-index-line"><span>Discovery → production</span><span aria-hidden="true">↗</span></div><p>Written to be revisited.<br>Built to connect the dots.</p></div></div></section>'''
        header = author_banner(library,route) + header
        featured = next((p for p in publications if p['id'] == library['site'].get('featuredPublicationId')), publications[0] if publications else None)
        if featured:
            header += f'''<section class="featured-publication"><div><span class="micro-label">FEATURED PUBLICATION / FIELD NOTES</span><h2>{esc(featured['title'])}</h2><p>{esc(featured['summary'])}</p><div class="featured-meta"><span>{esc(date_label(featured.get('publishedAt')))}</span><span>{featured['readingTime']} min read</span></div><a class="primary-action" href="{esc(publication_link(route,featured))}">Open the field guide <span aria-hidden="true">↗</span></a></div><div class="featured-art" aria-hidden="true"><span>THE DELIVERY LOOP</span><div class="delivery-loop">Discover <b>→</b> Build<br><b>↑</b><span>FDE</span><b>↓</b><br>Measure <b>←</b> Deploy</div><span>FROM PROBLEM TO OUTCOME</span></div></section>'''
        sections += f'<section class="library-section" id="latest"><div class="section-heading"><div><span class="micro-label">FRESH FROM THE LIBRARY</span><h2>Latest publications</h2></div><a class="text-action" href="{root_link(route,"publications/latest/")}">View all ↗</a></div><div class="publication-grid">{cards(publications[:3],library,route)}</div></section>'
        sections += f'<section class="library-section" id="topics"><div class="section-heading"><div><span class="micro-label">FOLLOW YOUR CURIOSITY</span><h2>Explore by domain</h2></div><span class="section-note">{len(library["taxonomy"]["categories"])} technical domains</span></div><div class="domain-grid">{topic_tiles(library,route)}</div></section>'
        sections += f'<section class="library-section" id="series"><div class="section-heading"><div><span class="micro-label">CONNECTED IDEAS</span><h2>Research & engineering series</h2></div></div><div class="collection-grid">{collection_cards("series",library,route)}</div></section>'
        sections += f'<section class="library-section" id="paths"><div class="section-heading"><div><span class="micro-label">A PROGRESSIVE READING PATH</span><h2>What should I learn next?</h2></div></div><div class="collection-grid">{collection_cards("paths",library,route)}</div></section>'
    elif kind == 'topics' and not category:
        title = 'Explore topics'
        header = f'<header class="library-page-heading"><span class="micro-label">TECHNICAL PUBLICATIONS</span><h1>Explore by domain.</h1><p>Follow a subject from first principles to production.</p></header><div class="domain-grid">{topic_tiles(library,route)}</div>'
    elif kind in {'series','paths'} and not collection:
        title = 'Publication series' if kind == 'series' else 'Learning paths'
        header = f'<header class="library-page-heading"><span class="micro-label">CONNECTED KNOWLEDGE</span><h1>{title}.</h1><p>Independent publications. A deliberate reading sequence.</p></header><div class="collection-grid">{collection_cards(kind,library,route)}</div>'
    else:
        title = category['title'] if category else collection['title'] if collection else 'Latest publications'
        description = category.get('description','') if category else collection['description'] if collection else 'The newest ideas in the engineering library.'
        header = f'<header class="library-page-heading"><span class="micro-label">TECHNICAL PUBLICATIONS</span><h1>{esc(title)}.</h1><p>{esc(description)}</p></header>'
    selected = publications
    if category:
        selected = [p for p in selected if category['id'] in category_memberships(p,{c['id']:c for c in library['taxonomy']['categories']})]
    if collection:
        selected = [next(p for p in publications if p['id'] == i) for i in collection['publicationIds']]
    index_heading = 'All publications' if kind == 'overview' else 'Publications'
    listing = f'''<section class="library-section" id="all-publications"><div class="section-heading"><div><span class="micro-label">THE COMPLETE INDEX</span><h2>{index_heading}</h2></div><span class="section-note" id="results-count" role="status" aria-live="polite">{len(selected)} publication{'s' if len(selected)!=1 else ''}</span></div>{controls(library,category['id'] if category else '',collection['id'] if collection and kind=='series' else '')}<div class="publication-grid" id="publication-results">{cards(selected,library,route)}</div></section>'''
    if collection:
        listing = listing.replace('id="publication-filters"', 'id="publication-filters" data-collection-ids="' + esc(json.dumps(collection['publicationIds'])) + '"')
        member_progress = [{'id': p['id'], 'reader': p['reader'], 'chapterSlugs': p.get('chapterSlugs',[])} for p in selected]
        ordered = ''.join(f'<li><span class="micro-label">{index+1:02}</span> <a href="{esc(publication_link(route,p))}">{esc(p["title"])}</a><span class="section-note">{p["readingTime"]} min read</span></li>' for index,p in enumerate(selected))
        header += f'<section class="collection-reading-order"><h2>Recommended reading order</h2><p class="collection-progress" data-collection-members="{esc(json.dumps(member_progress))}">Reading progress is available in this browser.</p><ol>{ordered}</ol></section>'
        if collection['id'] == 'research-to-reality':
            header = header.replace('</header>', '</header>' + research_series_intro(library, route), 1)
    return shell(library,route,title,description,header+sections+listing,active=kind if kind!='overview' else 'overview')


def article_page(library, publication, route, preview=False):
    p = publication
    available = {item['id']: item for item in library['publications']}
    breadcrumb = f'<a class="text-action" href="{root_link(route,"publications/")}">← Back to Publications</a>'
    category = next(c for c in library['taxonomy']['categories'] if c['id'] == p['primaryCategory'])
    type_title = next(t['title'] for t in library['taxonomy']['publicationTypes'] if t['id'] == p['publicationType'])
    category_url = root_link(route,'publications/topics/' + category['slug'] + '/')
    meta = []
    if p.get('author'):
        meta.append(esc(p['author']))
    if p.get('publishedAt'):
        meta.append('Published ' + esc(date_label(p['publishedAt'])))
    if p.get('updatedAt'):
        meta.append('Updated ' + esc(date_label(p['updatedAt'])))
    meta.append(f"{p['readingTime']} min read")
    if p.get('difficulty'):
        meta.append(esc(p['difficulty'].title()))
    if p.get('researchOrganization'):
        meta.append('Research focus: ' + esc(p['researchOrganization']))
        meta.append(f'Problem {p["problemNumber"]:02} / 20')
    tags = ''.join(f'<span class="article-tag">{esc(tag)}</span>' for tag in p.get('tags',[]))
    preview_notice = '<div class="article-notice" role="status">PRIVATE PREVIEW — unpublished content. This page is excluded from the production artifact.</div>' if preview else ''
    archive_notice = '<div class="article-notice" role="status">Archived publication. This permanent URL is retained for reference.</div>' if p['status']=='archived' else ''
    heading = f'''{breadcrumb}{preview_notice}{archive_notice}<header class="article-heading"><div class="article-classification"><span class="type-badge">{esc(type_title)}</span><a href="{category_url}">{esc(category['title'])}</a></div><h1>{esc(p['title'])}</h1>{f'<p class="article-subtitle">{esc(p["subtitle"])}</p>' if p.get('subtitle') else ''}<p class="article-meta">{'<span aria-hidden="true">·</span>'.join(meta)}</p><div class="article-tags">{tags}</div></header>'''
    if p.get('reader') == 'fde':
        body = heading + f'''<section class="fde-entry"><span class="micro-label">THE ORIGINAL CURRICULUM EXPERIENCE</span><h2>Follow the complete Field Guide.</h2><p>{esc(p['summary'])}</p><a class="primary-action" href="{root_link(route,'#end-to-end-fde-learning-map')}">Open FDE Field Guide ↗</a><p class="section-note">Your chapter progress and learning sequence carry on in the Field Guide reader.</p></section>'''
        return shell(library,route,p['title'],p['summary'],body,article=p)
    toc_items = [t for t in p['tableOfContents'] if t['level']>1]
    toc = ''.join(f'<a data-toc="{esc(t["id"])}" href="#{esc(t["id"])}" class="toc-level-{t["level"]}">{esc(t["title"])}</a>' for t in toc_items)
    prerequisites = '<aside class="prerequisite-box"><strong>Before you start</strong><ul>' + ''.join(f'<li>{esc(item)}</li>' for item in p.get('prerequisites',[])) + '</ul></aside>' if p.get('prerequisites') else ''
    content_html = __import__('re').sub(r'<h1\b[^>]*>.*?</h1>', '', p['html'], count=1, flags=__import__('re').S)
    student_intro, research_footer = '', ''
    if p.get('problemNumber'):
        from research_learning import knowledge_check, learning_panel
        cover = f'<figure class="article-cover"><img src="{esc(p["coverImage"])}" alt="{esc(p["coverAlt"])}" loading="eager" decoding="async"><figcaption>Figure from the supplied educational source package.</figcaption></figure>'
        heading += '<div class="article-series-badge">' + series_navigation(library,p,route) + '</div>' + cover
        student_intro = learning_panel(p)
        research_footer = knowledge_check(p)
        if p.get('diagramSupplementHtml'):
            research_footer += '<section class="diagram-supplements"><h2>Explore the supporting diagrams</h2>' + p['diagramSupplementHtml'] + '</section>'
        research_footer += '<section class="source-preservation"><h2>Sources and further study</h2><p>The illustrated article and supporting files are preserved from the supplied package. The learning introduction and knowledge checks are separate student additions. Site publication dates describe this library edition, not the original research release.</p><p><a href="README.md">Download the complete illustrated article source</a></p>' + p.get('originalSourceHtml','') + '</section>'
        package_groups = {name.split('/')[0] for name in p.get('packageFiles', []) if '/' in name}
        file_links = ''.join(f'<li><a href="{name}/">Browse {label}</a></li>' for name,label in [('assets','source figures'),('diagrams','editable diagram files'),('examples','example code'),('src','simulation code'),('tests','lab tests')] if name in package_groups)
        research_footer += '<nav class="package-downloads" aria-label="Learning source files"><ul>' + file_links + '</ul></nav>'
        # The original top heading moves to the shared article header.
        first_heading = next((t['id'] for t in p['tableOfContents'] if t['level'] == 1), '')
        heading = heading.replace('<h1>', '<h1 id="' + esc(first_heading) + '">', 1)
    abstract = f'<p class="article-abstract">{esc(p["abstract"])}</p>' if p.get('abstract') else ''
    links = p.get('repositoryLinks',[]) + p.get('researchReferences',[])
    references = '<section class="article-resources"><h2 id="resources">Resources and references</h2><ul>' + ''.join(f'<li><a href="{esc(link["url"])}" rel="noreferrer">{esc(link["label"])} ↗</a></li>' for link in links) + '</ul></section>' if links else ''
    related = [available[i] for i in p.get('relatedPublicationIds',[]) if i in available]
    related_html = f'<section class="library-section"><h2>Related publications</h2><div class="publication-grid">{cards(related,library,route)}</div></section>' if related else ''
    revisions = '<details class="revision-history"><summary>Revision history</summary><ul>' + ''.join(f'<li>{esc(date_label(item["date"]))}: {esc(item["summary"])} {esc(item.get("version"))}</li>' for item in p.get('revisions',[])) + '</ul></details>' if p.get('revisions') else ''
    body = f'''{heading}<div class="reading-progress" id="reading-progress" role="progressbar" aria-label="Reading position" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><span></span></div><div class="article-layout"><div><details class="mobile-article-toc"><summary>On this page</summary><nav aria-label="Article contents">{toc}</nav></details><article class="publication-prose" id="publication-body" data-publication-id="{esc(p['id'])}">{abstract}{prerequisites}{student_intro}{content_html}{references}{research_footer}</article>{revisions}<div class="article-completion"><span>Finished reading?</span><button id="complete-publication" data-publication-id="{esc(p['id'])}" type="button" aria-pressed="false" class="secondary-action">Mark as read</button></div><div id="article-series">{series_navigation(library,p,route)}</div>{related_html}</div><aside class="article-toc"><span class="micro-label">ON THIS PAGE</span><nav aria-label="Article contents">{toc}<a href="#student-start">Student starting point</a></nav></aside></div>'''
    return shell(library,route,p['title'],p['summary'],body,article=p)


def series_navigation(library, publication, route):
    by_id = {p['id']:p for p in library['publications']}
    collection = next((c for c in library['collections']['series'] if publication['id'] in c['publicationIds']),None)
    if not collection:
        return ''
    members = collection['publicationIds']
    index = members.index(publication['id'])
    links = []
    if index > 0:
        p = by_id[members[index-1]]
        links.append(f'<a href="{esc(publication_link(route,p))}"><small>Previous in series</small>{esc(p["title"])}</a>')
    if index+1 < len(members):
        p = by_id[members[index+1]]
        links.append(f'<a href="{esc(publication_link(route,p))}"><small>Next in series</small>{esc(p["title"])}</a>')
    return f'<section class="series-navigation"><a class="micro-label" href="{root_link(route,"publications/series/" + collection["slug"] + "/")}">{esc(collection["title"])} · Part {index+1} of {len(members)}</a><div>{"".join(links)}</div></section>'


def research_series_intro(library, route):
    groups = [('01–07', 'OpenAI research directions', 'Algorithms, mathematical physics, scientific agents, software, alignment, monitoring, and memory.'), ('08–16', 'Anthropic research', 'Interpretability, preferences, coordination, verification, optimization, and human judgment.'), ('17–19', 'Google DeepMind', 'Algorithm discovery, world models, and genome interpretation.'), ('20', 'NVIDIA physical AI', 'Simulation, robot policies, and the reality gap.')]
    parts = ''.join(f'<div><span class="micro-label">PROBLEMS {number}</span><h3>{title}</h3><p>{description}</p></div>' for number,title,description in groups)
    return f'''<section class="research-series-intro"><span class="micro-label">PUBLIC RESEARCH · OPEN CURIOSITY</span><p class="series-student-label">For students who want to understand—and try.</p><p>Start with an intuition. Learn the concepts. Trace the architecture. Question the evidence. Try a small experiment.</p><div class="research-parts">{parts}</div><details class="student-route-guide"><summary>New to these topics? Choose a starting path</summary><p>The subjects are advanced; you can begin with the student introductions and revisit the mathematics after building the prerequisites.</p><ul><li><a href="{root_link(route,'publications/paths/research-foundations/')}">Evidence, algorithms, and reliable AI</a></li><li><a href="{root_link(route,'publications/paths/scientific-ai/')}">Scientific AI: From hypotheses to checked evidence</a></li><li><a href="{root_link(route,'publications/paths/systems-to-physical-ai/')}">From coordinated systems to physical AI</a></li></ul></details></section>'''
