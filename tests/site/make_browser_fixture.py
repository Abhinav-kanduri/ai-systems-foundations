"""Create explicitly labeled test content outside production sources."""
import json
import shutil
import sys
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from build_publications import build
from fixture_content import copy_fixture_content

fixture=ROOT/'build/browser-source'
if fixture.exists():
    assert fixture.resolve().is_relative_to((ROOT/'build').resolve())
    shutil.rmtree(fixture)
fixture.mkdir(parents=True)
for folder in ('content','docs','assets'):
    if folder == 'content':
        copy_fixture_content(fixture/folder)
    else:
        shutil.copytree(ROOT/folder,fixture/folder)

def article(identity,title,category,status='published',published='2026-10-30',related=None):
    folder=fixture/'content/articles'/identity;folder.mkdir(parents=True)
    meta={'id':identity,'slug':identity,'title':title,'summary':'TEST FIXTURE ONLY. This publication is excluded from production.','primaryCategory':category,'publicationType':'technical-article','difficulty':'intermediate','status':status,'publishedAt':published,'tags':['Fixture'],'technologies':['CUDA'],'relatedPublicationIds':related or []}
    body='''# Test publication

## Memory hierarchy

TEST FIXTURE ONLY. A tensor-memory phrase for full-text search.

```python
def memory_bytes(elements):
    return elements * 4
```

## Equations

An illustrative expression: $x^2 + y^2$.

| Level | Purpose |
| --- | --- |
| Cache | Reuse |

## Trade-offs

'''+'\n\n'.join(['Fixture-only explanatory text for checking reading progress and layout. '*12]*18)+'''

## References

[Example reference](https://example.org).

<img src="assets/diagram.svg" alt="A fixture memory hierarchy">
<script>window.UNSAFE_FIXTURE = true</script>
'''
    (folder/'README.md').write_text('---\n'+json.dumps(meta)+'\n---\n'+body,encoding='utf-8')
    (folder/'assets').mkdir()
    (folder/'assets/diagram.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="120"><rect width="400" height="120" fill="#142136"/><text x="30" y="65" fill="#a8f35a">Fixture: memory hierarchy</text><script>alert(1)</script></svg>',encoding='utf-8')

article('test-gpu-memory','TEST FIXTURE: GPU Memory Hierarchy','gpu',related=['test-inference'])
article('test-inference','TEST FIXTURE: Inference Systems','ai-infrastructure')
article('test-draft-secret','TEST FIXTURE: PRIVATE DRAFT','gpu','draft')
article('test-future-secret','TEST FIXTURE: FUTURE','gpu','scheduled','2027-01-01T08:00:00Z')
article('test-archived','TEST FIXTURE: ARCHIVED','gpu','archived')
(fixture/'content/series/test-series.json').write_text(json.dumps({'id':'test-series','slug':'test-series','title':'TEST FIXTURE SERIES','description':'Fixture-only ordered collection.','status':'published','publicationIds':['test-gpu-memory','test-inference']}),encoding='utf-8')
(fixture/'content/learning-paths/test-path.json').write_text(json.dumps({'id':'test-path','slug':'test-path','title':'TEST FIXTURE PATH','description':'Fixture-only cross-category path.','status':'published','publicationIds':['test-inference','test-gpu-memory']}),encoding='utf-8')
build(fixture,fixture/'build/site',datetime(2026,10,31,23,tzinfo=timezone.utc))
print(f'Browser test artifact: {fixture / "build/site"}')
