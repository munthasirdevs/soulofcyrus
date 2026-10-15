const fs=require('fs'),vm=require('vm'),assert=require('assert');
const redirect=fs.readFileSync('dist/work/aftr/curved/index.html','utf8').match(/<script>(location.replace.*?)<\/script>/)[1];
for(const hash of ['', '#aftr', '#film', '#product/view']){
 let target;vm.runInNewContext(redirect,{location:{search:'?from=saved',hash,replace:url=>target=url}});
 assert.equal(target,'/work/aftr/?from=saved'+hash);
}
const data=JSON.parse(fs.readFileSync('dist/content.json')).projects[0].media;
for(const width of [390,1440]){
 let selected=-1,drawn=0,updated=0;const listeners={},location={hash:''};
 const dialog={open:false,close(){this.open=false}};
 const buttons=data.map((a,i)=>({dataset:{mediaId:a.id},click(){selected=i;dialog.open=true}}));
 const group={querySelectorAll:()=>buttons,_ribbon:{stage:{clientWidth:width},scroll:{scrollLeft:0},maxScroll:2600,step:200}};
 const document={querySelector:s=>s==='.lightbox'?dialog:group};
 vm.runInNewContext(fs.readFileSync('dist/aftr-route.js','utf8'),{document,location,addEventListener:(k,f)=>listeners[k]=f,drawRibbon:()=>drawn++,updateRibbonMedia:()=>updated++});
 for(const [i,a] of data.entries()){
  location.hash='#'+a.id+'/view';listeners.hashchange();assert.equal(selected,i);assert(dialog.open);
  location.hash='#'+a.id;listeners.popstate();assert(!dialog.open);
  assert(group._ribbon.scroll.scrollLeft>=0&&group._ribbon.scroll.scrollLeft<=2600);
 }
 location.hash='#%invalid';listeners.hashchange();
 assert(drawn===30&&updated===30);
}
console.log('PASS: legacy route redirects preserve queries/fragments; all 15 artwork and full-view deep links resolve at mobile/desktop widths; hash/popstate exits full view.');
