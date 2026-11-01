const {test,before,after}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'../..'), directory=path.join(root,'build/site');
let browser,server,base;
const report={articles:[],responsive:[],series:false};
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.md':'text/plain; charset=utf-8','.txt':'text/plain; charset=utf-8'};
before(async()=>{
 browser=await chromium.launch({headless:true});
 server=http.createServer((req,res)=>{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\/ai-systems-foundations\//,'/');
  if(pathname==='/favicon.ico'){res.writeHead(204);return res.end();}
  let file=path.resolve(directory,'.'+pathname);
  if(file!==directory&&!file.startsWith(directory+path.sep)){res.writeHead(403);return res.end();}
  if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
  if(!fs.existsSync(file)){res.writeHead(404);return res.end('Not found');}
  res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'text/plain'});res.end(fs.readFileSync(file));
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 base='http://127.0.0.1:'+server.address().port+'/ai-systems-foundations/';
 fs.mkdirSync(path.join(root,'build/qa'),{recursive:true});
});
after(async()=>{await browser?.close();server?.close();fs.writeFileSync(path.join(root,'build/qa/research-browser-results.json'),JSON.stringify(report,null,2));});
test('all twenty articles: sources, diagrams, mathematics, quizzes, images and ordered navigation',{timeout:240000},async()=>{
 const diagramErrors=[];
 for(let number=1;number<=20;number++){
  const id='research-problem-'+String(number).padStart(2,'0');
  const context=await browser.newContext({viewport:{width:1440,height:1000}});
  const page=await context.newPage();page.setDefaultTimeout(15000);
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  assert.equal((await page.goto(base+'publications/'+id+'/')).status(),200);
  assert.ok((await page.locator('h1').first().textContent()).includes(String(number).padStart(2,'0')));
  assert.equal(await page.locator('#student-start').count(),1);
  assert.equal(await page.locator('.source-preservation').count(),1);
  const images=await page.locator('#publication-body img, .article-cover img').evaluateAll(nodes=>nodes.map(n=>({src:n.src,alt:n.alt})));
  for(const img of images){assert.ok(img.alt,'image needs alt: '+id);if(img.src.startsWith(base))assert.equal((await page.request.get(img.src)).status(),200,img.src);}
  await page.locator('#publication-body img, .article-cover img').evaluateAll(nodes=>nodes.forEach(n=>n.loading='eager'));
  await page.waitForFunction(origin=>Array.from(document.querySelectorAll('#publication-body img, .article-cover img')).filter(n=>n.src.startsWith(origin)).every(n=>n.complete&&n.naturalWidth>0),base);
  // Open supplemental diagrams before checking every render; exact editable
  // sources remain available even when a renderer correction is required.
  await page.locator('.additional-diagram').evaluateAll(nodes=>nodes.forEach(n=>n.open=true));
  const figures=page.locator('.research-diagram');
  await figures.evaluateAll(nodes=>nodes.forEach(n=>{let parent=n.parentElement;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}}));
  assert.equal(await page.locator('math').evaluateAll(nodes=>nodes.filter(n=>n.getBoundingClientRect().width===0 && !n.closest('details:not([open])')).length),0,id+' invisible mathematics');
  for(let i=0;i<await figures.count();i++){
   const figure=figures.nth(i);
   await figure.locator('.expand-diagram').click();
   await page.locator('.diagram-dialog[open]').waitFor();
   if(await figure.getAttribute('data-rendered')!=='true')diagramErrors.push(id+' diagram '+i+': '+await figure.getAttribute('data-error'));
   else assert.ok(await figure.locator('.diagram-output svg').count());
   await page.keyboard.press('Escape');
  }
  const quiz=page.locator('.research-quiz');
  if(await quiz.count()){
   const correct=Number(await quiz.getAttribute('data-answer'));
   await quiz.locator('input').nth((correct+1)%await quiz.locator('input').count()).check();
   await quiz.locator('button[type=submit]').click();assert.equal(await quiz.getAttribute('data-result'),'incorrect');
   await quiz.locator('button[type=reset]').click();assert.equal(await quiz.locator('.quiz-feedback').textContent(),'');
   await quiz.locator('input').nth(correct).check();await quiz.locator('button[type=submit]').click();assert.equal(await quiz.getAttribute('data-result'),'correct');
  }else assert.ok(await page.locator('.knowledge-check details').count());
  assert.equal(await page.locator('#article-series a').count(),number===1||number===20?2:3);
  assert.deepEqual(errors,[],id);
  report.articles.push({id,diagrams:await figures.count(),rendererCorrections:await page.locator('.compatible-diagram-source').count(),math:await page.locator('math').count(),images:images.length,knowledgeCheck:await quiz.count()?'interactive':'reflection',passed:true});
  if(number===5){
   await context.grantPermissions(['clipboard-read','clipboard-write']);
   const copy=page.locator('.codehilite .code-copy button').first();
   await copy.click();await page.waitForFunction(()=>navigator.clipboard.readText().then(text=>text.length>0));
   assert.equal(await copy.textContent(),'Copied');
   await page.goto(base+'publications/'+id+'/');await page.screenshot({path:path.join(root,'build/qa/research-article-desktop.png')});
  }
  await context.close();
 }
 assert.deepEqual(diagramErrors,[]);
});
test('series discovery, organization search, filters, source download, and mobile reading',{timeout:90000},async()=>{
 const context=await browser.newContext({viewport:{width:1440,height:1000}}), page=await context.newPage();page.setDefaultTimeout(15000);
 await page.goto(base+'publications/series/research-to-reality/');
 assert.equal(await page.locator('.collection-reading-order li').count(),20);
 await page.locator('#publication-query').fill('NVIDIA');
 await page.waitForFunction(()=>document.querySelector('#results-count').textContent!=='20 publications');
 assert.equal(await page.locator('#publication-results [data-publication-id="research-problem-20"]').count(),1);
 await page.locator('#clear-filters').click();
 await page.locator('select[name=sort]').selectOption('recommended');
 await page.waitForFunction(()=>document.querySelectorAll('#publication-results .publication-card').length===20);
 const ids=await page.locator('#publication-results .publication-card').evaluateAll(nodes=>nodes.map(n=>n.dataset.publicationId));
 assert.deepEqual(ids,Array.from({length:20},(_,i)=>'research-problem-'+String(i+1).padStart(2,'0')));
 await page.evaluate(()=>window.scrollTo(0,0));
 await page.screenshot({path:path.join(root,'build/qa/research-series-desktop.png')});
 assert.equal((await page.request.get(base+'publications/research-problem-01/docs/original_uploaded_explanation.md')).status(),200);
 for(const width of [1440,768,390,320]){
  await page.setViewportSize({width,height:900});
  await page.goto(base+'publications/research-problem-13/');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'article overflow '+width);
  if(width<1150){await page.locator('.mobile-article-toc summary').click();await page.locator('.mobile-article-toc a').first().click();assert.ok(page.url().includes('#'));}
  if(width===390){await page.goto(base+'publications/research-problem-13/');await page.screenshot({path:path.join(root,'build/qa/research-article-mobile.png')});}
  report.responsive.push({width,passed:true});
 }
 report.series=true;await context.close();
});
