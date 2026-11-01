(function () {
  'use strict';
  const root = new URL(document.body.dataset.siteRoot, location.href);
  const status = document.createElement('span');
  status.className = 'sr-only'; status.setAttribute('role', 'status'); document.body.append(status);
  function addCopy(pre) {
    if (pre.closest('.original-transcript')) return;
    const toolbar = document.createElement('div'); toolbar.className = 'code-copy';
    const button = document.createElement('button'); button.type = 'button'; button.textContent = 'Copy code';
    button.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(pre.textContent); button.textContent = 'Copied'; status.textContent = 'Code copied to clipboard.'; }
      catch (_) { button.textContent = 'Select code to copy'; const range = document.createRange(); range.selectNodeContents(pre); const selection = getSelection(); selection.removeAllRanges(); selection.addRange(range); }
    });
    toolbar.append(button); pre.before(toolbar);
  }
  document.querySelectorAll('#publication-body pre').forEach(addCopy);
  document.querySelectorAll('.research-quiz').forEach(form => {
    const feedback = form.querySelector('.quiz-feedback');
    form.addEventListener('submit', event => {
      event.preventDefault(); const selected = new FormData(form).values().next().value;
      if (selected === undefined) return;
      const correct = selected === form.dataset.answer;
      const answer = form.querySelector('input[value="' + form.dataset.answer + '"]').closest('label').querySelector('span').textContent;
      feedback.textContent = (correct ? 'Correct. ' : 'Revisit your reasoning. ') + 'Answer: ' + answer + ' ' + form.dataset.explanation;
      form.dataset.result = correct ? 'correct' : 'incorrect';
    });
    form.addEventListener('reset', () => { feedback.textContent = ''; delete form.dataset.result; });
  });
  let libraryPromise, serial = Promise.resolve(), counter = 0;
  function loadMermaid() {
    if (!libraryPromise) libraryPromise = new Promise((resolve, reject) => {
      const script = document.createElement('script'); script.src = new URL('assets/vendor/mermaid/mermaid.min.js', root).href;
      script.onload = () => {
        window.mermaid.initialize({startOnLoad:false, securityLevel:'strict', theme:'default', suppressErrorRendering:true, flowchart:{htmlLabels:false, useMaxWidth:true}, sequence:{useMaxWidth:true}, maxTextSize:100000});
        resolve(window.mermaid);
      };
      script.onerror = () => reject(new Error('The local diagram library could not be loaded.')); document.head.append(script);
    });
    return libraryPromise;
  }
  async function render(figure) {
    if (figure.dataset.rendered) return;
    figure.dataset.rendered = 'pending';
    const output = figure.querySelector('.diagram-output'), source = figure.querySelector('code.language-mermaid').textContent;
    try {
      const mermaid = await loadMermaid();
      // Mermaid renders serially because its diagram registry is shared.
      // Quote node labels containing parentheses for Mermaid 11 compatibility;
      // keep the exact authored text in the editable source panel.
      const compatible = source.replace(/(\b[A-Za-z_][\w-]*)(\[|\{)(?!["\[])([^\]\}]*[()|][^\]\}]*)(\]|\})/g, (_,id,open,label,close)=>id+open+'"'+label.replace(/"/g,'&quot;').replace(/\r?\n/g,'<br/>')+'"'+close);
      if (compatible !== source) {
        figure.querySelector('figcaption').textContent = 'Architecture diagram · labels adjusted for renderer compatibility; both working and original sources are available below.';
        const details=document.createElement('details'), summary=document.createElement('summary'), pre=document.createElement('pre'), code=document.createElement('code');
        details.className='compatible-diagram-source';summary.textContent='View and copy working Mermaid source';code.textContent=compatible;
        pre.append(code);details.append(summary,pre);figure.append(details);addCopy(pre);
      }
      const result = await mermaid.render('research-diagram-' + (++counter), compatible);
      output.innerHTML = result.svg; figure.dataset.rendered = 'true';
      const svg = output.querySelector('svg'); svg.setAttribute('role','img'); svg.setAttribute('aria-label','Architecture diagram; editable Mermaid source is available below.');
    } catch (error) {
      output.textContent = 'This diagram could not render. The original source and source-package figures remain available below.';
      figure.dataset.rendered = 'error'; figure.dataset.error = String(error.message || error);
    }
  }
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { observer.unobserve(entry.target); serial = serial.then(() => render(entry.target)); }
  }), {rootMargin:'500px'});
  const dialog = document.createElement('dialog'); dialog.className = 'diagram-dialog'; dialog.setAttribute('aria-labelledby','expanded-diagram-title');
  dialog.innerHTML = '<header><h2 id="expanded-diagram-title">Explore the diagram</h2><button type="button">Close diagram</button></header><p>Scroll to inspect the full diagram.</p><div class="diagram-output"></div>';
  document.body.append(dialog);
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) { const r=dialog.getBoundingClientRect(); if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close(); } });
  document.querySelectorAll('.research-diagram').forEach(figure => {
    observer.observe(figure);
    figure.querySelector('.expand-diagram').addEventListener('click', async () => {
      serial = serial.then(() => render(figure)); await serial;
      dialog.querySelector('.diagram-output').replaceChildren(...Array.from(figure.querySelector('.diagram-output').childNodes, n=>n.cloneNode(true)));
      dialog.showModal();
    });
  });
})();
