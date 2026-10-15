// Preserve saved AFTR artwork links after selecting the curved presentation.
(()=>{
 const group=document.querySelector('.aftr-curved .ribbon-group');
 if(!group)return;
 const buttons=[...group.querySelectorAll('.gallery-open')];
 function readLocation(){
  let fragment;try{fragment=decodeURIComponent(location.hash.slice(1));}catch{return;}
  const view=fragment.endsWith('/view'),id=view?fragment.slice(0,-5):fragment;
  const index=buttons.findIndex(button=>button.dataset.mediaId===id);
  const dialog=document.querySelector('.lightbox');
  if(dialog?.open)dialog.close();
  if(index<0)return;
  const state=group._ribbon;
  const base=Math.min(state.stage.clientWidth<=700?1:3,(buttons.length-1)/2);
  state.scroll.scrollLeft=Math.max(0,Math.min(state.maxScroll,(index-base)*state.step));
  drawRibbon(group);updateRibbonMedia();
  if(view)buttons[index].click();
 }
 addEventListener('hashchange',readLocation);
 addEventListener('popstate',readLocation);
 readLocation();
})();
