const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const v=document.querySelector('#hero-video');
if(v){const play=document.querySelector('#play'),sound=document.querySelector('#sound');const sync=()=>{play.textContent=v.paused?'Play':'Pause';play.setAttribute('aria-label',(v.paused?'Play':'Pause')+' homepage video');sound.textContent=v.muted?'Sound off':'Sound on';sound.setAttribute('aria-pressed',String(!v.muted));};play.addEventListener('click',()=>{if(v.paused)v.play().catch(()=>{});else v.pause();});sound.addEventListener('click',()=>{v.muted=!v.muted;sync();});v.addEventListener('play',sync);v.addEventListener('pause',sync);if(reduced){v.autoplay=false;v.pause();sync();}}
// Every film starts muted; simultaneous autoplay must not pause other films.
// If a visitor enables sound, keep the other films playing silently.
const films=[...document.querySelectorAll('video')];
films.forEach(video=>video.addEventListener('volumechange',()=>{if(!video.muted)films.forEach(other=>{if(other!==video)other.muted=true;});}));
// Muted thumbnail films respect reduced motion and pause off-screen.
const thumbs=[...document.querySelectorAll('.thumbnail-video')];
if(reduced){thumbs.forEach(video=>{video.autoplay=false;video.pause();});}
else if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>entries.forEach(({target,isIntersecting})=>{if(isIntersecting)target.play().catch(()=>{});else target.pause();}),{threshold:.1});thumbs.forEach(video=>observer.observe(video));}
// A single keyboard-accessible lightbox, scoped to the selected album.
const openers=[...document.querySelectorAll('.gallery-open')];
if(openers.length){
 const box=document.createElement('dialog');box.className='lightbox';box.setAttribute('aria-label','Enlarged image gallery');
 box.innerHTML='<div class="lightbox-inner"><div class="lightbox-bar"><span class="lightbox-count"></span><button class="lightbox-close" type="button" autofocus>Close ×</button></div><div class="lightbox-stage"><button class="lightbox-arrow lightbox-prev" type="button" aria-label="Previous image">‹</button><img class="lightbox-image" alt=""><button class="lightbox-arrow lightbox-next" type="button" aria-label="Next image">›</button></div><p class="lightbox-caption"></p></div>';
 document.body.appendChild(box);let group=[],index=0,trigger=null,oldOverflow='';
 const img=box.querySelector('img'),caption=box.querySelector('.lightbox-caption'),count=box.querySelector('.lightbox-count');
 function show(i){index=(i+group.length)%group.length;const el=group[index];img.src=el.dataset.full;img.alt=el.querySelector('img').alt;caption.textContent=el.dataset.caption;count.textContent=String(index+1).padStart(2,'0')+' / '+String(group.length).padStart(2,'0');}
 openers.forEach(button=>button.addEventListener('click',()=>{trigger=button;group=[...button.closest('.gallery-grid').querySelectorAll('.gallery-open')];show(group.indexOf(button));oldOverflow=document.body.style.overflow;document.body.style.overflow='hidden';box.showModal();}));
 box.querySelector('.lightbox-close').addEventListener('click',()=>box.close());box.querySelector('.lightbox-prev').addEventListener('click',()=>show(index-1));box.querySelector('.lightbox-next').addEventListener('click',()=>show(index+1));
 box.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();show(index+1);}if(e.key==='ArrowLeft'){e.preventDefault();show(index-1);}});
 box.addEventListener('close',()=>{document.body.style.overflow=oldOverflow;trigger?.focus();});
 box.querySelector('.lightbox-stage').addEventListener('click',e=>{if(e.target.classList.contains('lightbox-stage'))box.close();});
 let touchX=null;img.addEventListener('touchstart',e=>{touchX=e.changedTouches[0].clientX;},{passive:true});img.addEventListener('touchend',e=>{if(touchX!==null){const delta=e.changedTouches[0].clientX-touchX;if(Math.abs(delta)>55)show(index+(delta<0?1:-1));touchX=null;}},{passive:true});
}

if(reduced)document.querySelectorAll('video[controls][autoplay]').forEach(video=>{video.autoplay=false;video.pause();});

// Load the decorative About film only near the section. Respect motion preferences
// and retain the visitor's pause choice when the section leaves/re-enters view.
const aboutVideo=document.querySelector('#about-video');
if(aboutVideo){
 const aboutSection=document.querySelector('#about'),aboutButton=document.querySelector('#about-playback');
 const motionPreference=matchMedia('(prefers-reduced-motion: reduce)');
 let aboutVisible=false,aboutUserPaused=false,aboutLoaded=false;
 const syncAbout=()=>{aboutButton.textContent=aboutVideo.paused?'Play background':'Pause background';aboutButton.setAttribute('aria-label',(aboutVideo.paused?'Play':'Pause')+' About background video');};
 const updateAbout=()=>{
  aboutButton.hidden=motionPreference.matches;
  if(motionPreference.matches||!aboutVisible||aboutUserPaused||document.hidden){aboutVideo.pause();syncAbout();return;}
  if(!aboutLoaded){const source=aboutVideo.querySelector('source');source.src=source.dataset.src;aboutVideo.load();aboutLoaded=true;}
  aboutVideo.muted=true;aboutVideo.play().catch(syncAbout);
 };
 aboutVideo.addEventListener('play',syncAbout);aboutVideo.addEventListener('pause',syncAbout);
 aboutButton.addEventListener('click',()=>{aboutUserPaused=!aboutVideo.paused;updateAbout();});
 motionPreference.addEventListener('change',updateAbout);document.addEventListener('visibilitychange',updateAbout);
 if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{aboutVisible=entries[0].isIntersecting;updateAbout();},{rootMargin:'300px 0px'});observer.observe(aboutSection);}
 else{aboutVisible=true;}
 updateAbout();
}
