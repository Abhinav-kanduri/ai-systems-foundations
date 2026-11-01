"""Import the supplied research packages without rewriting their source material.

The ignored ZIPs are required only for initial import and the optional source audit.
Normal website builds use the committed article files and preservation manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SERIES = 'research-to-reality'
TOPICS = [
    ('fundamentals', 'Algorithm discovery, computational complexity, and the difference between empirical speedups and mathematical proof.', ['Algorithms and asymptotic complexity', 'Basic Boolean logic']),
    ('research', 'Explore AI-assisted mathematical physics, fluid equations, and why successful simulations cannot establish a universal theorem.', ['Calculus and differential equations', 'Numerical simulation basics']),
    ('distributed-systems', 'Learn how scientific agents coordinate hypotheses, evidence, provenance, and independent experimental validation.', ['Basic scientific method', 'APIs and distributed workflows']),
    ('fundamentals', 'Study cross-language software modernization through behavioral equivalence, differential testing, and independent correctness evidence.', ['Python fundamentals', 'Unit tests and software interfaces']),
    ('reliability', 'Understand reward hacking: why improving a proxy score can leave the real objective unmet, and how independent evaluation helps.', ['Basic machine learning', 'Evaluation metrics']),
    ('reliability', 'Design agent monitoring and intervention around observable behavior, precision and recall, and controls before tool execution.', ['AI agent and tool-call basics', 'Precision and recall']),
    ('generative-ai', 'Explore agent memory, retrieval, changing facts, provenance, and correction through a practical long-term memory scenario.', ['Retrieval and embeddings', 'Basic data storage']),
    ('ai-ml', 'Connect transformer internals, superposition, and activation patching to the challenge of explaining model behavior.', ['Neural network basics', 'Transformer attention and linear algebra']),
    ('ai-ml', 'Examine how agents elicit preferences, represent uncertainty, and help people choose without treating a proxy as their true intent.', ['Basic decision-making concepts', 'Ranking and evaluation']),
    ('distributed-systems', 'Learn multi-agent coordination through shared resources, conflicting actions, synchronization, and measurable system outcomes.', ['Concurrent programming basics', 'Queues and transactions']),
    ('fundamentals', 'Distinguish tests from proofs and study specifications, invariants, proof assistants, and a small transfer-contract lab.', ['Programming and logic', 'Preconditions and postconditions']),
    ('research', 'Follow mathematical discovery from patterns and conjectures to formalization, proof checking, and reproducible evidence.', ['Mathematical proof basics', 'Willingness to explore Lean']),
    ('gpu', 'Study GPU optimization through memory traffic, kernel fusion, correctness gates, and the limits of benchmark speedups.', ['Python and numerical arrays', 'Basic GPU execution and memory']),
    ('research', 'Explore quantum circuit optimization through gate cancellation, equivalence checks, and hardware-aware cost models.', ['Linear algebra and complex numbers', 'Qubits and quantum gates']),
    ('research', 'Learn how AI can assist drug-development research while separating computational predictions from experimental and clinical evidence.', ['Basic biology and scientific method', 'Uncertainty and multi-objective ranking']),
    ('reliability', 'Investigate automation bias and human oversight with evidence-first review, independent judgment, and an interface experiment.', ['Basic evaluation and experimental design', 'Human review workflows']),
    ('research', 'Explore AlphaEvolve-style algorithm search: generate candidates, evaluate correctness and fitness, and retain measurable improvements.', ['Python fundamentals', 'Algorithms and benchmark design']),
    ('robotics', 'Connect world models, state transitions, feedback, and replanning through a small CPU-only control experiment.', ['Python fundamentals', 'States, actions, and feedback control']),
    ('ai-ml', 'Explore genome interpretation and variant prioritization while distinguishing predicted molecular effects from evidence of causation.', ['Basic DNA and gene regulation', 'Prediction, uncertainty, and validation']),
    ('robotics', 'Connect physical-world simulation, vision-language-action policies, and sim-to-real evaluation in NVIDIA physical AI research.', ['Machine learning basics', 'Robotics perception and control']),
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def content_elements(text):
    # Count the entire source, protecting fenced code before section discovery.
    fences = re.findall(r'(?ms)^```([^\n]*)\n(.*?)^```\s*$', text)
    prose = re.sub(r'(?ms)^```[^\n]*\n.*?^```\s*$', '', text)
    sections = []
    matches = list(re.finditer(r'(?m)^(#{1,6}) (.+)$', prose))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(prose)
        section = prose[match.start():end]
        sections.append({'heading': match[2], 'level': len(match[1]), 'sha256': digest(section.encode()), 'characters': len(section)})
    return {
        'sections': sections,
        'tables': len(re.findall(r'(?m)^\|\s*:?-{3}', text)),
        'codeBlocks': len(fences),
        'mermaidBlocks': sum(language.strip() == 'mermaid' for language, _ in fences),
        'mathDelimiters': {key: text.count(key) for key in ('$$', '\\[', '\\(', '$')},
        'references': list(dict.fromkeys(re.findall(r'https?://[^\s<>\)\]"\']+', text))),
        'images': re.findall(r'!\[[^\]]*\]\(([^)]+)\)|<img[^>]*src=["\']([^"\']+)', text),
    }


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def import_sources(published_at):
    archives = sorted((ROOT / 'Research-opensource').glob('*.zip'))
    manifest = {'seriesId': SERIES, 'sitePublicationDate': published_at, 'articles': [], 'omittedFiles': [], 'missingProblems': []}
    for archive in archives:
        number = int(re.search(r'Problem_(\d+)', archive.name)[1])
        folder = ROOT / 'content/articles' / f'research-problem-{number:02}'
        if folder.exists():
            raise ValueError(f'Refusing to overwrite existing article: {folder}')
        with zipfile.ZipFile(archive) as package:
            names = [i.filename for i in package.infolist() if not i.is_dir()]
            main = min((n for n in names if n.endswith('README.md')), key=lambda n: len(n.split('/')))
            prefix = str(PurePosixPath(main).parent)
            prefix = '' if prefix == '.' else prefix + '/'
            files = []
            for item in package.infolist():
                if item.is_dir():
                    continue
                relative = PurePosixPath(item.filename.removeprefix(prefix))
                if relative.is_absolute() or '..' in relative.parts or '\\' in str(relative) or ':' in str(relative) or stat.S_ISLNK(item.external_attr >> 16):
                    raise ValueError(f'Unsafe ZIP entry: {item.filename}')
                if '__pycache__' in relative.parts or relative.suffix == '.pyc':
                    manifest['omittedFiles'].append({'archive': archive.name, 'entry': item.filename, 'reason': 'Generated Python bytecode; source retained'})
                    continue
                data = package.read(item)
                target = folder.joinpath(*relative.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                files.append({'archiveEntry': item.filename, 'path': target.relative_to(ROOT).as_posix(), 'sha256': digest(data), 'bytes': len(data)})
            body = package.read(main).decode('utf-8-sig')
        title = re.search(r'(?m)^# (.+)$', body)[1].strip()
        category, summary, prerequisites = TOPICS[number - 1]
        organization = 'OpenAI' if number <= 7 else 'Anthropic' if number <= 16 else 'Google DeepMind' if number <= 19 else 'NVIDIA'
        images = re.findall(r'!\[([^\]]*)\]\((assets/[^)]+)\)', body)
        images = [(alt, src) for alt, src in images if 'logo' not in src.lower()]
        if not images:
            images = [(p.stem.replace('-', ' '), p.relative_to(folder).as_posix()) for p in (folder / 'assets').rglob('*.png') if 'logo' not in p.name]
        cover_alt, cover = images[0]
        metadata = {
            'id': f'research-problem-{number:02}', 'slug': f'research-problem-{number:02}',
            'title': title, 'summary': summary, 'primaryCategory': category,
            'secondaryCategories': [c for c in ('research', 'ai-ml') if c != category],
            'publicationType': 'research-analysis', 'difficulty': 'advanced',
            'status': 'published', 'publishedAt': published_at,
            'seriesId': SERIES, 'seriesOrder': number, 'problemNumber': number,
            'researchOrganization': organization, 'coverImage': cover, 'coverAlt': cover_alt,
            'tags': [organization, 'Research to Reality', 'Student learning', 'Public research'],
            'prerequisites': prerequisites,
            'relatedPublicationIds': [f'research-problem-{i:02}' for i in (number - 1, number + 1) if 1 <= i <= 20],
        }
        originals = [f['path'] for f in files if re.search(r'original|source_text|source_article', f['path'], re.I) and not f['path'].endswith('.py')]
        metadata['packageFiles'] = [str(Path(f['path']).relative_to(folder.relative_to(ROOT))).replace('\\', '/') for f in files]
        metadata['originalSources'] = [str(Path(f).relative_to(folder.relative_to(ROOT))).replace('\\', '/') for f in originals]
        write_json(folder / 'publication.json', metadata)
        manifest['articles'].append({
            'number': number, 'title': title, 'archive': archive.name, 'archiveSha256': digest(archive.read_bytes()),
            'mainSource': main, 'articleSource': (folder / 'README.md').relative_to(ROOT).as_posix(),
            'route': f'/publications/research-problem-{number:02}/', 'organization': organization,
            'files': files, 'originalEducationalSources': originals, 'elements': content_elements(body),
            'preservation': 'All imported file bytes match the source package; generated caches excluded.',
        })
    manifest['missingProblems'] = sorted(set(range(1, 21)) - {a['number'] for a in manifest['articles']})
    manifest['articles'].sort(key=lambda a: a['number'])
    write_json(ROOT / 'docs/research-publications/source-manifest.json', manifest)
    ids = [f'research-problem-{a["number"]:02}' for a in manifest['articles']]
    write_json(ROOT / 'content/series/research-to-reality.json', {
        'id': SERIES, 'slug': SERIES, 'title': 'Research to Reality — 20 AI Research Problems',
        'description': 'An independent student learning series based on publicly available research. Explore the intuition, theory, architectures, evidence, and open questions, with original figures, practical challenges, and links to primary sources. Research organizations identify the work discussed; they do not endorse this series.',
        'status': 'published', 'publicationIds': ids,
    })
    paths = [
        ('research-foundations', 'Start here: Evidence, algorithms, and reliable AI', 'Begin with algorithms, software correctness, evaluation, and human oversight. Read the prerequisites first; each article includes an intuition and a challenge.', [1, 4, 5, 6, 7, 16]),
        ('scientific-ai', 'Scientific AI: From hypotheses to checked evidence', 'Study scientific collaboration, mathematical proof, interpretability, preferences, drug research, and genome interpretation. Follow original references and distinguish predictions from established evidence.', [2, 3, 8, 9, 11, 12, 15, 19]),
        ('systems-to-physical-ai', 'From coordinated systems to physical AI', 'Connect multi-agent coordination, GPU and quantum optimization, algorithm search, world models, and robotics. Check the hardware and dependency notes before running a lab.', [10, 13, 14, 17, 18, 20]),
    ]
    for identity, title, description, numbers in paths:
        write_json(ROOT / f'content/learning-paths/{identity}.json', {'id': identity, 'slug': identity, 'title': title, 'description': description, 'status': 'published', 'publicationIds': [f'research-problem-{n:02}' for n in numbers if n not in manifest['missingProblems']]})
    print(f'Imported {len(ids)} complete packages. Missing: {manifest["missingProblems"]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--published-at', required=True, help='Actual site publication date, not an inferred research date')
    import_sources(parser.parse_args().published_at)
