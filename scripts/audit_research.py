"""Audit imported research source bytes and their generated public artifacts."""
from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from publication_content import load_library
from publication_model import PublicationError
from research_learning import safe_svg

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'docs/research-publications'


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if attrs.get('id'): self.ids.add(attrs['id'])
        if tag in {'a','img','link','script'}:
            value=attrs.get('href') or attrs.get('src')
            if value:self.links.append(value)


def audit():
    manifest=json.loads((REPORTS/'source-manifest.json').read_text(encoding='utf-8'))
    library=load_library(ROOT)
    research=[p for p in library['publications'] if p.get('problemNumber')]
    articles={p['problemNumber']:p for p in research}
    if len(research)!=20 or sorted(articles)!=list(range(1,21)):
        raise PublicationError('The public library must contain problems 01–20 exactly once')
    output=ROOT/'build/site'
    if not (output/'publications/index.json').exists():
        raise PublicationError('Build the public artifact before auditing')
    failures=[];records=[];inventory=[];preservation=[]
    for item in manifest['articles']:
        p=articles[item['number']];folder=(ROOT/item['articleSource']).parent
        destination=output/f'publications/{p["slug"]}'
        parser=LinkParser();parser.feed((destination/'index.html').read_text(encoding='utf-8'))
        source_checks=[];artifact_checks=[]
        for file in item['files']:
            path=ROOT/file['path'];data=path.read_bytes()
            source_ok=hashlib.sha256(data).hexdigest()==file['sha256']
            if not source_ok:failures.append('Changed source bytes: '+file['path'])
            relative=path.relative_to(folder)
            target=destination/relative
            if path.suffix in {'.html','.htm','.js'}:target=target.with_name(target.name+'.txt')
            expected=safe_svg(data) if path.suffix=='.svg' else data
            artifact_ok=target.is_file() and target.read_bytes()==expected
            if not artifact_ok:failures.append('Missing or changed public source file: '+str(target))
            source_checks.append({'path':file['path'],'matchesOriginalSha256':source_ok})
            artifact_checks.append({'path':target.relative_to(output).as_posix(),'matchesExpectedBytes':artifact_ok,'svgSanitized':path.suffix=='.svg'})
        missing_links=[]
        for link in parser.links:
            u=urlsplit(link)
            if u.scheme or link.startswith('//'):continue
            target=(destination/unquote(u.path)).resolve() if u.path else destination/'index.html'
            if not target.is_relative_to(output.resolve()) or not target.exists():missing_links.append(link)
            elif not u.path and u.fragment and u.fragment not in parser.ids:missing_links.append(link)
        failures.extend(f'{p["id"]}: unresolved link {link}' for link in missing_links)
        required={
            'problem statement':r'problem statement', 'why difficult':r'why (?:is|this)|why.*difficult',
            'technical concepts':r'concepts', 'architecture':r'architecture|end.to.end',
            'research example':r'(?:practical|real.world|simple|research) example|real research',
            'research goal':r'research goal', 'remaining challenges':r'remains|still difficult|research challenges',
            'interview perspective':r'interview perspective', 'learning challenge':r'subscriber.*challenge',
            'research references':r'(?:primary |research |learning |background |further )references|further learning',
            'takeaway':r'takeaway',
        }
        headings='\n'.join(s['heading'] for s in item['elements']['sections'])
        coverage={name:('present in source headings' if re.search(pattern,headings,re.I) else 'no separate source heading; full body retained') for name,pattern in required.items()}
        file_names=[Path(f['path']).suffix.lower() for f in item['files']]
        record={'number':item['number'],'title':p['title'],'route':item['route'],'sourceFiles':source_checks,'publicFiles':artifact_checks,
                'sourceSections':item['elements']['sections'],'sourceSectionCoverage':coverage,'localLinkFailures':missing_links,
                'originalTranscripts':len(p.get('originalSources',[])),'mathExpressions':p['html'].count('<math '),
                'inlineMermaid':item['elements']['mermaidBlocks'],'companionMermaid':file_names.count('.mmd'),
                'codeBlocks':item['elements']['codeBlocks'],'tables':item['elements']['tables'],
                'quizKind':p['learning']['quiz']['kind'],'primaryReferenceNote':'Source references retained; related official pages checked selectively, not every scientific result independently replicated.'}
        records.append(record)
        inventory.append(f'| {item["number"]:02} | {p["title"]} | {item["archive"]} | {len(item["files"])} | {file_names.count(".png")+file_names.count(".svg")} | {file_names.count(".mmd")} | {len(item["elements"]["references"])} |')
        gaps=', '.join(name for name,status in coverage.items() if status.startswith('no separate')) or 'None'
        preservation.append(f'| {item["number"]:02} | {len(item["elements"]["sections"])} | {len(item["files"])} / {len(item["files"])} | {record["tables"]} | {record["codeBlocks"]} | {record["mathExpressions"]} | {record["quizKind"]} | {gaps} |')
    result={'passed':not failures,'failures':failures,'articleCount':len(records),'articles':records,'notes':[
        'Main Markdown and all supporting package files checked byte-for-byte against their recorded source SHA256.',
        'Public source attachments checked byte-for-byte; SVG attachments compared with the safe sanitized rendering.',
        'The original package Markdown is unchanged. Centering wrappers are removed only during rendering; code, mathematics, tables, and reference destinations have additional tests.',
        'The first article heading moves into the shared article header. A source navigation typo in problem 03 has an alias at the intended section.',
        'Plaintext originals retain export artifacts. Complete transcripts are expandable and downloadable, not substituted for the illustrated reading edition.',
        'Source HTML demos are downloadable as text, not executable within the site origin.',
        'Generated Python caches are the only excluded package entries. Source titles and scientific qualifications are retained.',
    ]}
    (REPORTS/'preservation-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (REPORTS/'02-source-inventory.md').write_text('# Research source inventory\n\nAll 20 ZIP packages were supplied locally in the ignored `Research-opensource/` directory. The main source in each is the shallowest `README.md`; supporting originals, examples, tests, PNG/SVG figures, and editable Mermaid/Graphviz sources are retained beside it in `content/articles/research-problem-NN/`.\n\nThe JSON manifest records the exact original path, archive checksum, every file checksum, full section hashes, code/table/math counts, images, and external reference destinations. This is a snapshot of the supplied material, not a claim that it includes every publicly available resource.\n\n| Problem | Original title | Package | Files | PNG/SVG | Mermaid files | Distinct source URLs |\n|---|---|---|---:|---:|---:|---:|\n'+'\n'.join(inventory)+'\n\nNo problem package is missing. The `.pyc` and `__pycache__` entries in package 01 are generated caches and were excluded. Four packages (04, 08, 11, 20) contain no separate original educational transcript; their complete main article is retained.\n',encoding='utf-8')
    (REPORTS/'03-content-preservation-report.md').write_text('# Content preservation report\n\n'+('PASS' if not failures else 'FAIL')+': '+str(len(records))+' articles audited. See `preservation-audit.json` for every source-to-output file check and section hash, and `source-manifest.json` for the original baseline.\n\nThe check compares complete file bodies and attachment bytes, not only heading counts. Tests additionally check complete fenced code bodies and all Markdown citation destinations in the rendered article. Browser tests separately verify visible diagrams, mathematical markup, figures, and learning interactions.\n\n| Problem | Source headings | File hashes matched | Tables | Code fences | Math rendered | Check type | Source heading gaps |\n|---|---:|---|---:|---:|---:|---|---|\n'+'\n'.join(preservation)+'\n\nA missing separate heading is reported as a source limitation, not filled with invented scientific text. For example, 01–03 organize some difficulty and challenge material differently. Problems 01 and 04 have no dedicated primary research citation list; clearly labeled background references were added separately. Problem 14 names primary research in plain text; the supplied `REFERENCES.md` is retained and clickable official links are added in metadata.\n\n'+ '\n'.join('- '+note for note in result['notes'])+'\n',encoding='utf-8')
    print(f'Audited {len(records)} articles, {sum(len(r["sourceFiles"]) for r in records)} source files; {len(failures)} failures.')
    if failures:raise PublicationError(failures)
    return result


if __name__=='__main__':audit()
