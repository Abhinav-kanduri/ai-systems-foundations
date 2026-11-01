"""Validated student supplements for the independently authored research series."""
from __future__ import annotations

import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote, urlsplit

from publication_model import PublicationError


def safe_svg(data):
    tree = ET.fromstring(data)
    for parent in tree.iter():
        for child in list(parent):
            tag = child.tag.split('}')[-1].lower()
            if tag in {'script', 'foreignobject', 'iframe', 'object', 'embed'} or (tag == 'style' and re.search(r'@import|url\s*\(|expression\s*\(', child.text or '', re.I)):
                parent.remove(child)
        for key, value in list(parent.attrib.items()):
            name = key.split('}')[-1].lower()
            if name.startswith('on') or name in {'href', 'src'} and (urlsplit(value.strip()).scheme or value.strip().startswith('//')) or name == 'style' and re.search(r'url\s*\(|expression\s*\(', value, re.I):
                del parent.attrib[key]
    return ET.tostring(tree)


def local_file(folder, name):
    target = (folder / name).resolve()
    if not target.is_relative_to(folder.resolve()) or not target.is_file():
        raise PublicationError(f'Research source path is missing or leaves its article: {name}')
    return target


def validate_learning(learning):
    for key in ('intuition', 'learningGoal', 'exerciseNote'):
        if not isinstance(learning.get(key), str) or not learning[key].strip():
            raise PublicationError(f'Learning supplement needs {key}')
    quiz = learning.get('quiz', {})
    if not isinstance(quiz.get('question'), str) or not quiz['question'].strip():
        raise PublicationError('Knowledge check needs a question')
    if quiz.get('kind') == 'reflection':
        if not quiz.get('explanation'):
            raise PublicationError('Reflection check needs an explanation')
    else:
        choices = quiz.get('choices', [])
        answer = quiz.get('answer')
        if not isinstance(choices, list) or not 2 <= len(choices) <= 6 or not all(isinstance(c, str) and c.strip() for c in choices):
            raise PublicationError('Knowledge check needs two to six answer choices')
        if type(answer) is not int or not 0 <= answer < len(choices) or not quiz.get('explanation'):
            raise PublicationError('Knowledge check has an invalid answer mapping')


def enrich_research(publication, folder):
    from publication_content import render_markdown
    try:
        learning = json.loads((folder / 'learning.json').read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as error:
        raise PublicationError(f'Missing or invalid research learning supplement: {folder.name}') from error
    validate_learning(learning)
    publication['learning'] = learning
    local_file(folder, publication['coverImage'])
    publication['originalSourceHtml'] = ''
    for name in publication.get('originalSources', []):
        original = local_file(folder, name).read_text(encoding='utf-8-sig')
        publication['originalSourceHtml'] += ('<details class="original-transcript"><summary>Read the complete original educational transcript: ' + html.escape(name)
            + '</summary><p>This unchanged transcript may include exported formatting or diagram text. The illustrated article above is the package’s edited reading version.</p>'
            + '<a href="' + quote(name) + '">Download original source</a><pre>' + html.escape(original) + '</pre></details>')
    included = {re.sub(r'\s+', '', s) for s in re.findall(r'(?ms)^```mermaid\s*\n(.*?)^```\s*$', publication['body'])}
    supplements = []
    for name in publication.get('packageFiles', []):
        if name.endswith('.mmd'):
            source = local_file(folder, name).read_text(encoding='utf-8-sig')
            if re.sub(r'\s+', '', source) not in included:
                rendered, _ = render_markdown('```mermaid\n' + source + '\n```\n')
                supplements.append('<details class="additional-diagram"><summary>' + html.escape(Path(name).stem.replace('-', ' ').replace('_', ' ')) + '</summary>' + rendered + '</details>')
    publication['diagramSupplementHtml'] = ''.join(supplements)
    # Original interactive HTML remains downloadable as text, without executing
    # arbitrary source-package scripts in the publication origin.
    publication['html'] = re.sub(r'href="([^"]+\.html?)"', r'href="\1.txt"', publication['html'])
    # This source heading accidentally runs into its first sentence. Keep its
    # authored text, and add an alias for the original navigation destination.
    if publication['problemNumber'] == 3:
        publication['html'] = re.sub(r'(?=<h[2-6] id="5-practical-example)', '<span id="5-practical-example"></span>', publication['html'], count=1)


def learning_panel(p):
    learning = p['learning']
    esc = lambda value: html.escape(str(value), quote=True)
    return f'''<section class="student-intro" aria-labelledby="student-start"><span class="micro-label">A STUDENT’S STARTING POINT</span><h2 id="student-start">Build your understanding, one question at a time.</h2><p class="student-intuition">{esc(learning['intuition'])}</p><dl><dt>What you’ll learn</dt><dd>{esc(learning['learningGoal'])}</dd><dt>Try it yourself</dt><dd>{esc(learning['exerciseNote'])}</dd></dl><p class="source-context">Independent educational material based on publicly available resources. {esc(p['researchOrganization'])} identifies the research discussed, not an affiliation or endorsement. Public access does not imply an open-source license.</p></section>'''


def knowledge_check(p):
    esc = lambda value: html.escape(str(value), quote=True)
    quiz = p['learning']['quiz']
    identifier = p['id'] + '-check'
    if quiz.get('kind') == 'reflection':
        return f'''<section class="knowledge-check"><span class="micro-label">CHECK YOUR UNDERSTANDING</span><h2>Pause and explain</h2><p>{esc(quiz['question'])}</p><p>Write or say your reasoning before opening the explanation.</p><details><summary>Compare your reasoning</summary><p>{esc(quiz['explanation'])}</p></details></section>'''
    choices = ''.join(f'<label class="quiz-choice"><input type="radio" name="{identifier}" value="{i}" required><span>{esc(choice)}</span></label>' for i, choice in enumerate(quiz['choices']))
    return f'''<section class="knowledge-check"><span class="micro-label">CHECK YOUR UNDERSTANDING</span><h2>Apply what you learned</h2><form class="research-quiz" data-answer="{quiz['answer']}" data-explanation="{esc(quiz['explanation'])}"><fieldset><legend>{esc(quiz['question'])}</legend>{choices}</fieldset><div class="quiz-actions"><button type="submit">Check answer</button><button type="reset">Try again</button></div><p class="quiz-feedback" role="status" aria-live="polite"></p><noscript><p>Enable JavaScript to check answers interactively, or use the explanation below.</p></noscript></form><details><summary>Answer and explanation</summary><p>{esc(quiz['choices'][quiz['answer']])}</p><p>{esc(quiz['explanation'])}</p></details></section>'''
