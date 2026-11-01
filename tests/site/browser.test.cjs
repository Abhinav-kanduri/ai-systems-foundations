const {test,before,after} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname,'../..');
let browser,publicServer,fixtureServer,publicUrl,fixtureUrl;
const outputs=[];
const mime={'.html':'text/html; charset=utf-8','.json':'application/json; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.md':'text/plain; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.xml':'application/xml'};
async function server(directory) {
  const instance=http.createServer((request,response)=>{
    let pathname=decodeURIComponent(new URL(request.url,'http://localhost').pathname);
    if(pathname==='/favicon.ico'){response.writeHead(204);return response.end();}
    if(pathname.startsWith('/project/'))pathname=pathname.slice(8);
    const target=path.resolve(directory,'.'+pathname);
    if(!target.startsWith(directory+path.sep)&&target!==directory){response.writeHead(403);return response.end();}
    const file=fs.existsSync(target)&&fs.statSync(target).isDirectory()?path.join(target,'index.html'):target;
    if(!fs.existsSync(file)||!fs.statSync(file).isFile()){response.writeHead(404);return response.end('Not found');}
    response.writeHead(200,{'Content-Type':mime[path.extname(file)]||'text/plain'});response.end(fs.readFileSync(file));
  });
  await new Promise(resolve=>instance.listen(0,'127.0.0.1',resolve));
  return [instance,'http://127.0.0.1:'+instance.address().port];
}
before(async()=>{
  browser=await chromium.launch({headless:true});
  [publicServer,publicUrl]=await server(path.join(root,'build/site'));
  [fixtureServer,fixtureUrl]=await server(path.join(root,'build/browser-source/build/site'));
  fs.mkdirSync(path.join(root,'build/qa'),{recursive:true});
});
after(async()=>{await browser?.close();publicServer?.close();fixtureServer?.close();fs.writeFileSync(path.join(root,'reports/publications/browser-results.json'),JSON.stringify(outputs,null,2)+'\n');});
async function pageFor(url,width=1440,height=1000) {
  const context=await browser.newContext({viewport:{width,height},reducedMotion:'reduce'});
  const page=await context.newPage();page.setDefaultTimeout(7000);
  await page.goto(url);return {page,context};
}
test('production library, source-driven counts, routes, metadata and FDE entry',async()=>{
  const {page,context}=await pageFor(publicUrl+'/publications/');
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await page.locator('#publication-results [data-publication-id="fde-field-guide"]').waitFor();
  assert.match(await page.locator('h1').innerText(),/Explore\.\nEngineer\.\nDiscover\./);
  assert.equal(await page.locator('.domain-tile').count(),12);
  assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),'https://abhinav-kanduri.github.io/ai-systems-foundations/publications/');
  assert.ok(await page.locator('script[type="application/ld+json"]').count());
  await page.screenshot({path:path.join(root,'build/qa/publications-desktop.png')});
  await page.locator('#publication-query').fill('Customer discovery');
  assert.equal(await page.locator('#publication-results .publication-card').count(),1);
  await page.locator('#publication-query').fill('impossible-no-match-1281');
  await page.locator('#publication-results .library-empty').waitFor();
  assert.ok(page.url().includes('q=impossible'));
  await page.locator('#clear-filters').click();
  await page.locator('#publication-results .publication-card').waitFor();
  await page.locator('#publication-results .text-action').click();
  await page.locator('#chapter-nav a').first().waitFor();
  assert.equal(await page.locator('#progress-total').textContent(),'27');
  assert.equal(await page.locator('.fde-publications-link').count(),1);
  assert.deepEqual(errors,[]);
  await context.close();outputs.push({scenario:'Production library and FDE entry',passed:true});
});
test('new articles, full-text search, combined filters, empty states and URL state',async()=>{
  const {page,context}=await pageFor(fixtureUrl+'/publications/');
  await page.locator('#results-count').filter({hasText:'3 publications'}).waitFor();
  await page.locator('#publication-query').fill('tensor-memory');
  await page.locator('select[name=topic]').selectOption('gpu');
  await page.locator('select[name=type]').selectOption('technical-article');
  await page.locator('select[name=difficulty]').selectOption('intermediate');
  await page.locator('select[name=year]').selectOption('2026');
  await page.locator('select[name=reading]').selectOption('medium');
  await page.locator('select[name=series]').selectOption('test-series');
  await page.locator('#publication-results [data-publication-id="test-gpu-memory"]').waitFor();
  assert.equal(await page.locator('#publication-results .publication-card').count(),1);
  await page.reload();
  await page.locator('#publication-results [data-publication-id="test-gpu-memory"]').waitFor();
  assert.equal(await page.locator('select[name=topic]').inputValue(),'gpu');
  assert.equal(await page.locator('#publication-query').inputValue(),'tensor-memory');
  await page.locator('select[name=difficulty]').selectOption('advanced');
  await page.locator('#publication-results .library-empty').waitFor();
  await context.close();outputs.push({scenario:'Article discovery, full-text search and composed URL filters',passed:true});
});
test('draft and future publication protection includes direct URLs, feeds and indexes',async()=>{
  const {page,context}=await pageFor(fixtureUrl+'/publications/');
  for(const identity of ['test-draft-secret','test-future-secret']) {
    assert.equal((await page.request.get(fixtureUrl+'/publications/'+identity+'/')).status(),404);
    for(const route of ['/publications/index.json','/publications/feed.xml','/sitemap.xml'])assert.ok(!(await (await page.request.get(fixtureUrl+route)).text()).includes(identity));
  }
  assert.equal((await page.request.get(fixtureUrl+'/content/articles/test-draft-secret/README.md')).status(),404);
  await page.goto(fixtureUrl+'/publications/test-archived/');
  await page.getByText('Archived publication.',{exact:false}).waitFor();
  await context.close();outputs.push({scenario:'Draft/future protection and archive retention',passed:true});
});
test('article renderer, anchors, code, math, references, related and series navigation',async()=>{
  const {page,context}=await pageFor(fixtureUrl+'/publications/test-gpu-memory/');
  assert.ok(await page.locator('.codehilite').count());
  assert.ok(await page.locator('math').count());
  assert.ok(await page.locator('.publication-prose table').count());
  assert.equal(await page.evaluate(()=>window.UNSAFE_FIXTURE),undefined);
  assert.equal(await page.locator('.publication-prose script').count(),0);
  await page.locator('.article-toc a[href="#equations"]').click();
  assert.ok(page.url().endsWith('#equations'));
  await page.screenshot({path:path.join(root,'build/qa/article-desktop.png')});
  assert.equal(await page.locator('.series-navigation a').count(),2);
  assert.ok(await page.locator('.library-section [data-publication-id="test-inference"]').count());
  await page.locator('#complete-publication').click();
  assert.equal(await page.locator('#complete-publication').getAttribute('aria-pressed'),'true');
  await page.reload();await page.locator('#complete-publication[aria-pressed=true]').waitFor();
  await page.goto(fixtureUrl+'/publications/series/test-series/');
  await page.locator('[data-collection-members]').filter({hasText:'1 of 2'}).waitFor();
  assert.deepEqual(await page.locator('.collection-reading-order li a').allTextContents(),['TEST FIXTURE: GPU Memory Hierarchy','TEST FIXTURE: Inference Systems']);
  await page.goto(fixtureUrl+'/publications/paths/test-path/');
  assert.equal((await page.locator('.collection-reading-order li a').allTextContents())[0],'TEST FIXTURE: Inference Systems');
  await context.close();outputs.push({scenario:'Article rendering and explicit completion/series/path navigation',passed:true});
});
test('publication navigation and completion preserve existing FDE progress byte-for-byte',async()=>{
  const {page,context}=await pageFor(fixtureUrl+'/');
  await page.locator('#chapter-nav a').first().waitFor();
  const seed='["1-fde-mindset-and-role-fundamentals","manually-maintained-state"]';
  await page.evaluate(value=>localStorage.setItem('fde-field-guide-progress-v1',value),seed);
  await page.goto(fixtureUrl+'/publications/');
  await page.goto(fixtureUrl+'/publications/test-gpu-memory/');
  await page.locator('#complete-publication').click();
  assert.equal(await page.evaluate(()=>localStorage.getItem('fde-field-guide-progress-v1')),seed);
  await page.goto(fixtureUrl+'/#1-fde-mindset-and-role-fundamentals');
  await page.locator('#complete-button.is-complete').waitFor();
  assert.equal(await page.locator('#progress-count').textContent(),'1');
  assert.equal(await page.evaluate(()=>localStorage.getItem('fde-field-guide-progress-v1')),seed);
  await context.close();outputs.push({scenario:'Existing FDE progress preservation',passed:true});
});
test('responsive desktop, tablet, mobile, keyboard navigation and project subpath',async()=>{
  for(const [width,height] of [[1440,1000],[768,1024],[390,844],[320,740]]) {
    const {page,context}=await pageFor(publicUrl+'/project/publications/',width,height);
    await page.locator('#publication-results .publication-card').waitFor();
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'overflow at '+width);
    if(width<=850) {
      await page.locator('#library-menu').click();
      assert.equal(await page.locator('#library-menu').getAttribute('aria-expanded'),'true');
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('#library-menu').getAttribute('aria-expanded'),'false');
      await page.screenshot({path:path.join(root,'build/qa/publications-'+width+'.png')});
    }
    const unnamed=await page.locator('button').evaluateAll(buttons=>buttons.filter(b=>!b.textContent.trim()&&!b.getAttribute('aria-label')).length);
    assert.equal(unnamed,0);
    await page.keyboard.press('Tab');
    assert.ok(await page.evaluate(()=>document.activeElement!==document.body));
    await context.close();
  }
  outputs.push({scenario:'Responsive 1440/768/390/320, keyboard and project subpath',passed:true});
});
test('mobile article reading, safe diagrams and practical contrast in both themes',async()=>{
  const {page,context}=await pageFor(fixtureUrl+'/publications/test-gpu-memory/',390,844);
  await page.locator('.mobile-article-toc summary').click();
  await page.locator('.mobile-article-toc a[href="#equations"]').click();
  assert.ok(page.url().endsWith('#equations'));
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  const svg=await (await page.request.get(fixtureUrl+'/publications/test-gpu-memory/assets/diagram.svg')).text();
  assert.ok(!svg.includes('<script'));
  await page.screenshot({path:path.join(root,'build/qa/article-mobile.png')});
  for(const theme of ['dark','light']) {
    await page.evaluate(theme=>document.documentElement.dataset.theme=theme,theme);
    const ratios=await page.evaluate(()=>{
      const style=getComputedStyle(document.body);
      const luminance=hex=>{const rgb=hex.trim().replace('#','').match(/../g).map(n=>parseInt(n,16)/255).map(c=>c<=.04045?c/12.92:((c+.055)/1.055)**2.4);return rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;};
      const contrast=(a,b)=>{const x=luminance(style.getPropertyValue(a)),y=luminance(style.getPropertyValue(b));return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);};
      return [contrast('--text','--bg'),contrast('--text-soft','--bg'),contrast('--accent','--bg')];
    });
    assert.ok(ratios.every(r=>r>=4.5),theme+' contrast '+ratios);
  }
  await context.close();outputs.push({scenario:'Mobile article, safe SVG and dark/light token contrast',passed:true});
});
