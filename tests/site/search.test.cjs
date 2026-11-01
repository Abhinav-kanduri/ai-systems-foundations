const test = require('node:test');
const assert = require('node:assert/strict');
const {select} = require('../../docs/assets/publication-search.js');
const articles = [
  {id:'a',title:'GPU architecture',summary:'Hardware',primaryCategory:'gpu',secondaryCategories:['ai'],publicationType:'technical-article',difficulty:'advanced',publishedAt:'2026-10-30',readingTime:12,tags:['CUDA'],searchText:'A tensor memory phrase'},
  {id:'b',title:'Systems',summary:'GPU architecture in production',primaryCategory:'ai',publicationType:'tutorial',publishedAt:'2026-10-31',readingTime:35,searchText:'Latency matters'},
  {id:'c',title:'Basics',summary:'Intro',primaryCategory:'gpu',publicationType:'engineering-notes',publishedAt:'2025-01-01',updatedAt:'2026-11-01',readingTime:5,searchText:'Begin here'}
];
const taxonomy={categories:[{id:'gpu',title:'Accelerator Architecture'},{id:'ai',title:'Artificial Intelligence'}]};
const collections={series:[{id:'s',publicationIds:['c','a']}]};
test('searches body, category and tags',()=>{ assert.equal(select(articles,{q:'tensor memory'})[0].id,'a');assert.equal(select(articles,{q:'cuda'})[0].id,'a');assert.equal(select(articles,{q:'accelerator' },taxonomy).length,2); });
test('title ranks before incidental mentions',()=>assert.equal(select(articles,{q:'GPU architecture'})[0].id,'a'));
test('filters compose',()=>assert.deepEqual(select(articles,{topic:'gpu',type:'technical-article',difficulty:'advanced',year:'2026',reading:'medium'}).map(p=>p.id),['a']));
test('secondary categories match',()=>assert.equal(select(articles,{topic:'ai'}).length,2));
test('sort variants are deterministic',()=>{assert.deepEqual(select(articles,{sort:'oldest'}).map(p=>p.id),['c','a','b']);assert.equal(select(articles,{sort:'updated'})[0].id,'c');assert.equal(select(articles,{sort:'title'})[0].id,'c');});
test('series uses explicit recommended order',()=>assert.deepEqual(select(articles,{series:'s',sort:'recommended'},taxonomy,collections).map(p=>p.id),['c','a']));
test('learning path scope remains independent of filters',()=>assert.deepEqual(select(articles,{collectionIds:['c'],topic:'gpu'}).map(p=>p.id),['c']));
test('empty results',()=>assert.equal(select(articles,{q:'not-in-any-publication'}).length,0));
test('parent topic includes configured subcategory',()=>assert.equal(select(articles,{topic:'hardware'},{categories:[{id:'gpu',title:'GPU',parentId:'hardware'},{id:'hardware',title:'Hardware'}]}).length,2));
test('explicit sorting overrides relevance ranking',()=>assert.equal(select(articles,{q:'GPU architecture',sort:'latest'})[0].id,'b'));
