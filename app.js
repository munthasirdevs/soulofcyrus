let reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const v = document.querySelector('#hero-video');
if (v) { const play = document.querySelector('#play'), sound = document.querySelector('#sound'); const sync = () => { play.textContent = v.paused ? 'Play' : 'Pause'; play.setAttribute('aria-label', (v.paused ? 'Play' : 'Pause') + ' homepage video'); sound.textContent = v.muted ? 'Sound off' : 'Sound on'; sound.setAttribute('aria-pressed', String(!v.muted)); }; play.addEventListener('click', () => { if (v.paused) v.play().catch(() => { }); else v.pause(); }); sound.addEventListener('click', () => { v.muted = !v.muted; sync(); }); v.addEventListener('play', sync); v.addEventListener('pause', sync); if (reduced) { v.autoplay = false; v.pause(); sync(); } }
// Every film starts muted; simultaneous autoplay must not pause other films.
// If a visitor enables sound, keep the other films playing silently.
const films = [...document.querySelectorAll('video')];
films.forEach(video => video.addEventListener('volumechange', () => { if (!video.muted) films.forEach(other => { if (other !== video) other.muted = true; }); }));
// Muted thumbnail films respect reduced motion and pause off-screen.
const thumbs = [...document.querySelectorAll('.thumbnail-video')];
if (reduced) { thumbs.forEach(video => { video.autoplay = false; video.pause(); }); }
else if ('IntersectionObserver' in window) { const observer = new IntersectionObserver(entries => entries.forEach(({ target, isIntersecting }) => { if (isIntersecting && !reduced) target.play().catch(() => { }); else target.pause(); }), { threshold: .1 }); thumbs.forEach(video => observer.observe(video)); }

if (reduced) document.querySelectorAll('video[controls][autoplay]').forEach(video => { video.autoplay = false; video.pause(); });

// Load the decorative About film only near the section. Respect motion preferences
// and retain the visitor's pause choice when the section leaves/re-enters view.
const aboutVideo = document.querySelector('#about-video');
if (aboutVideo) {
    const aboutSection = document.querySelector('#about'), aboutButton = document.querySelector('#about-playback');
    const motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
    let aboutVisible = false, aboutUserPaused = false, aboutLoaded = false;
    const syncAbout = () => { aboutButton.textContent = aboutVideo.paused ? 'Play background' : 'Pause background'; aboutButton.setAttribute('aria-label', (aboutVideo.paused ? 'Play' : 'Pause') + ' About background video'); };
    const updateAbout = () => {
        aboutButton.hidden = motionPreference.matches;
        if (motionPreference.matches || !aboutVisible || aboutUserPaused || document.hidden) { aboutVideo.pause(); syncAbout(); return; }
        if (!aboutLoaded) { const source = aboutVideo.querySelector('source'); source.src = source.dataset.src; aboutVideo.load(); aboutLoaded = true; }
        aboutVideo.muted = true; aboutVideo.play().catch(syncAbout);
    };
    aboutVideo.addEventListener('play', syncAbout); aboutVideo.addEventListener('pause', syncAbout);
    aboutButton.addEventListener('click', () => { aboutUserPaused = !aboutVideo.paused; updateAbout(); });
    motionPreference.addEventListener('change', updateAbout); document.addEventListener('visibilitychange', updateAbout);
    if ('IntersectionObserver' in window) { const observer = new IntersectionObserver(entries => { aboutVisible = entries[0].isIntersecting; updateAbout(); }, { rootMargin: '300px 0px' }); observer.observe(aboutSection); }
    else { aboutVisible = true; }
    updateAbout();
}

// Compact navigation. Escape, outside clicks and route changes dismiss it.
const menuButton = document.querySelector('.menu-toggle'), siteMenu = document.querySelector('.site-menu');
function closeMenu(returnFocus = false) { if (!menuButton) return; siteMenu.hidden = true; menuButton.setAttribute('aria-expanded', 'false'); menuButton.setAttribute('aria-label', 'Open navigation'); if (returnFocus) menuButton.focus(); }
menuButton?.addEventListener('click', () => { const open = siteMenu.hidden; siteMenu.hidden = !open; menuButton.setAttribute('aria-expanded', String(open)); menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation'); });
siteMenu?.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
document.addEventListener('pointerdown', e => { if (!e.target.closest('.site-header')) closeMenu(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !siteMenu?.hidden) { closeMenu(true); e.preventDefault(); } });

// Full-viewport, scroll-driven concave ribbon. The camera recedes in the middle;
// image pixels themselves are never skewed, and modal images have no perspective.
const ribbonGroups = [...document.querySelectorAll('.ribbon-group')];
let currentRibbon = null, lightboxOpen = false, ribbonUserPaused = reduced;
const motionButton = document.querySelector('.gallery-motion');
const dock = document.querySelector('.project-dock'), aboutToggle = document.querySelector('.dock-about'), details = document.querySelector('.dock-details');
const progress = document.querySelector('.gallery-progress'), range = document.querySelector('.gallery-range');
const previous = document.querySelector('.gallery-prev'), next = document.querySelector('.gallery-next');
function setAbout(open) { if (!dock) return; details.hidden = !open; dock.classList.toggle('expanded', open); aboutToggle.textContent = open ? '[ CLOSE ]' : '[ ABOUT ]'; aboutToggle.setAttribute('aria-expanded', String(open)); }
aboutToggle?.addEventListener('click', () => setAbout(details.hidden));
document.addEventListener('keydown', e => { if (e.key === 'Escape' && dock?.classList.contains('expanded') && !lightboxOpen) { setAbout(false); aboutToggle.focus(); } });
function updateRibbonMedia() { ribbonGroups.forEach(g => g.querySelectorAll('video').forEach(video => { const visible = g === currentRibbon && !document.hidden && !lightboxOpen && !ribbonUserPaused && !video.closest('.ribbon-card').hidden; if (visible) video.play().catch(() => { }); else video.pause(); })); }
function drawRibbon(g) {
    const st = g._ribbon; if (!st) return;
    const W = st.stage.clientWidth, H = st.stage.clientHeight, mobile = W <= 700, n = st.cards.length;
    const value = st.scroll.scrollLeft / Math.max(1, st.maxScroll), base = Math.min(mobile ? 1 : 3, (n - 1) / 2);
    const center = base + value * Math.max(0, n - 1 - base);
    const h = Math.min(mobile ? 257 : 327, mobile ? W * .47 : W * .192, H * (mobile ? .77 : .55));
    const w = h * .703;
    st.cards.forEach((card, i) => {
        const d = i - center, ad = Math.abs(d), limit = mobile ? 2.6 : 4.7, show = ad < limit;
        card.hidden = !show;
        const opener = card.querySelector('.gallery-open'); opener.tabIndex = show ? 0 : -1;
        if (!show) return;
        const x = mobile ? W * (.385 * d + .005 * d * d * d) : W * (.137 * d + .0027 * d * d * d);
        const scale = 1 + (mobile ? .12 : .073) * d * d;
        const angle = Math.max(-44, Math.min(44, -d * (mobile ? 17 : 11)));
        card.style.width = w + 'px'; card.style.height = h + 'px'; card.style.setProperty('--card-ratio', w / h);
        card.style.transform = `translate(-50%,-50%) translateX(${x}px) rotateY(${angle}deg) scale(${scale})`;
        card.style.zIndex = String(Math.round(100 + ad * 10));
    });
    if (g === currentRibbon) {
        const pct = Math.max(0, Math.min(100, value * 100)); progress.textContent = Math.round(pct) + '%'; range.value = pct; range.setAttribute('aria-valuetext', Math.round(pct) + ' percent through ' + g.dataset.title);
        previous.disabled = pct < .05; next.disabled = pct > 99.95;
    }
}
function sizeRibbon(g) {
    const st = g._ribbon, old = st.maxScroll ? st.scroll.scrollLeft / st.maxScroll : 0;
    st.step = Math.max(160, st.stage.clientWidth * .18);
    const base = Math.min(st.stage.clientWidth <= 700 ? 1 : 3, (st.cards.length - 1) / 2);
    st.maxScroll = Math.max(1, (st.cards.length - 1 - base) * st.step);
    st.track.style.width = (st.stage.clientWidth + st.maxScroll) + 'px';
    st.scroll.scrollLeft = old * st.maxScroll; drawRibbon(g);
}
function moveRibbon(amount, absolute = false) { if (!currentRibbon) return; const s = currentRibbon._ribbon; const target = absolute ? amount * s.maxScroll : s.scroll.scrollLeft + amount * s.step; s.scroll.scrollTo({ left: Math.max(0, Math.min(s.maxScroll, target)), behavior: reduced ? 'instant' : 'smooth' }); }
function activateRibbon(id, announce = false) {
    const g = ribbonGroups.find(x => x.id === id) || ribbonGroups[0]; if (!g) return;
    const changedWhileViewing = lightboxOpen && g !== currentRibbon; if (changedWhileViewing) document.querySelector('.lightbox')?.close();
    ribbonGroups.forEach(x => x.hidden = x !== g); currentRibbon = g;
    document.querySelectorAll('[data-album]').forEach(a => { a.setAttribute('aria-current', String(a.dataset.album === g.id)); });
    document.querySelector('.dock-summary').textContent = g.dataset.intro;
    document.querySelector('.detail-project').textContent = g.dataset.title;
    document.querySelector('.detail-format').textContent = g.dataset.format;
    document.querySelector('.detail-focus').textContent = g.dataset.focus;
    sizeRibbon(g); updateRibbonMedia();
    motionButton.hidden = !g.querySelector('video'); motionButton.setAttribute('aria-pressed', String(ribbonUserPaused)); motionButton.textContent = ribbonUserPaused ? 'Play films' : 'Pause films';
    if (changedWhileViewing) document.querySelector('[data-album="' + g.id + '"]')?.focus({ preventScroll: true });
    if (announce) document.querySelector('.gallery-announcement').textContent = g.dataset.title + ', ' + g._ribbon.cards.length + ' works.';
}
ribbonGroups.forEach(g => {
    const stage = g.querySelector('.ribbon-stage'), scroll = g.querySelector('.ribbon-scroll'), cards = [...g.querySelectorAll('.ribbon-card')];
    g._ribbon = { stage, scroll, cards, track: g.querySelector('.ribbon-track'), maxScroll: 0, step: 200 };
    let frame = 0;
    scroll.addEventListener('scroll', () => { if (!frame) frame = requestAnimationFrame(() => { frame = 0; drawRibbon(g); updateRibbonMedia(); }); }, { passive: true });

    stage.addEventListener('keydown', e => { if (e.target.tagName === 'INPUT') return; if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); moveRibbon(e.key === 'ArrowRight' ? 1 : -1); } if (e.key === 'Home' || e.key === 'End') { e.preventDefault(); moveRibbon(e.key === 'Home' ? 0 : 1, true); } });
    let startX = 0, startY = 0, startScroll = 0, dragging = false, moved = false, pointer = null, suppressUntil = 0;
    stage.addEventListener('pointerdown', e => { if (e.button !== 0 || e.isPrimary === false) return; startX = e.clientX; startY = e.clientY; startScroll = scroll.scrollLeft; dragging = true; moved = false; pointer = e.pointerId; });
    stage.addEventListener('pointermove', e => { if (!dragging || e.pointerId !== pointer) return; const dx = e.clientX - startX, dy = e.clientY - startY; if (!moved && Math.abs(dx) + Math.abs(dy) < 7) return; if (!moved && Math.abs(dy) > Math.abs(dx) && e.pointerType !== 'mouse' && stage.clientWidth > 700) { dragging = false; return; } moved = true; stage.classList.add('dragging'); if (!stage.hasPointerCapture(pointer)) stage.setPointerCapture(pointer); scroll.scrollLeft = startScroll - dx * (stage.clientWidth <= 700 ? 1.6 : 1.3); });
    const finish = () => { if (moved) suppressUntil = performance.now() + 350; dragging = false; stage.classList.remove('dragging'); if (pointer !== null && stage.hasPointerCapture(pointer)) stage.releasePointerCapture(pointer); pointer = null; };
    stage.addEventListener('pointerup', finish); stage.addEventListener('pointercancel', finish); stage.addEventListener('lostpointercapture', () => { dragging = false; stage.classList.remove('dragging'); });
    stage.addEventListener('click', e => { if (performance.now() < suppressUntil) { e.preventDefault(); e.stopImmediatePropagation(); } }, true);
});
if (ribbonGroups.length) {
    activateRibbon(decodeURIComponent(location.hash.slice(1)));
    document.querySelector('.ribbon-main').addEventListener('wheel', e => { if (e.ctrlKey || lightboxOpen || siteMenu && !siteMenu.hidden || e.target.closest('input,textarea,select,[contenteditable]')) return; e.preventDefault(); const delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY; currentRibbon._ribbon.scroll.scrollLeft += delta * (e.deltaMode === 1 ? 18 : e.deltaMode === 2 ? innerWidth : 1); }, { passive: false });
    motionButton.addEventListener('click', () => { ribbonUserPaused = !ribbonUserPaused; motionButton.textContent = ribbonUserPaused ? 'Play films' : 'Pause films'; motionButton.setAttribute('aria-pressed', String(ribbonUserPaused)); updateRibbonMedia(); });
    document.querySelectorAll('[data-album]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); history.pushState(null, '', '#' + a.dataset.album); activateRibbon(a.dataset.album, true); }));
    addEventListener('hashchange', () => activateRibbon(decodeURIComponent(location.hash.slice(1)), true));
    addEventListener('popstate', () => activateRibbon(decodeURIComponent(location.hash.slice(1)), true));
    previous.addEventListener('click', () => moveRibbon(-1)); next.addEventListener('click', () => moveRibbon(1));
    range.addEventListener('input', () => { currentRibbon._ribbon.scroll.scrollLeft = Number(range.value) / 100 * currentRibbon._ribbon.maxScroll; });
    document.addEventListener('visibilitychange', updateRibbonMedia);
    let resizeTimer; addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => { if (currentRibbon) sizeRibbon(currentRibbon); }, 80); });
}

// One accessible, full-viewport image/film viewer, scoped to the active album.
const openers = [...document.querySelectorAll('.gallery-open')];
if (openers.length) {
    const box = document.createElement('dialog'); box.className = 'lightbox'; box.setAttribute('aria-label', 'Full-view gallery');
    box.innerHTML = '<div class="lightbox-inner"><div class="lightbox-bar"><span class="lightbox-count" aria-live="polite"></span><button class="lightbox-close" type="button" autofocus>[ CLOSE × ]</button></div><div class="lightbox-stage"><button class="lightbox-arrow lightbox-prev" type="button" aria-label="Previous work">‹</button><div class="lightbox-media"><img class="lightbox-image" alt=""><video class="lightbox-video" controls muted playsinline preload="metadata" hidden></video></div><button class="lightbox-arrow lightbox-next" type="button" aria-label="Next work">›</button></div><p class="lightbox-caption"></p></div>';
    document.body.appendChild(box);
    let group = [], index = 0, trigger = null, oldOverflow = '', rotation = 0;
    const img = box.querySelector('img'), movie = box.querySelector('video'), caption = box.querySelector('.lightbox-caption'), count = box.querySelector('.lightbox-count'), mediaStage = box.querySelector('.lightbox-media');
    function fit() {
        if (rotation !== 90 || img.hidden) return; const W = mediaStage.clientWidth, H = mediaStage.clientHeight, iw = Number(group[index]?.dataset.width) || img.naturalWidth, ih = Number(group[index]?.dataset.height) || img.naturalHeight;
        if (!iw || !ih) return; const scale = Math.min(H / iw, W / ih); img.style.width = iw * scale + 'px'; img.style.height = ih * scale + 'px';
    }
    function show(i) {
        movie.pause(); movie.removeAttribute('src'); movie.load();
        index = (i + group.length) % group.length; const el = group[index], isVideo = el.dataset.type === 'video';
        movie.hidden = !isVideo; img.hidden = isVideo; rotation = Number(el.dataset.rotation) || 0;
        img.classList.toggle('is-rotated', rotation === 90); img.style.width = ''; img.style.height = '';
        if (isVideo) { const vSrc = el.querySelector('video source')?.getAttribute('src') || el.querySelector('video')?.getAttribute('src') || el.dataset.full; movie.src = vSrc; movie.muted = true; movie.poster = el.querySelector('video')?.poster || ''; if (!reduced && !ribbonUserPaused) movie.play().catch(() => { }); }
        else { const iSrc = el.querySelector('img')?.getAttribute('src') || el.dataset.full; img.src = iSrc; img.alt = el.querySelector('img')?.alt || ''; requestAnimationFrame(fit); }
        caption.textContent = el.dataset.caption || ''; count.textContent = String(index + 1).padStart(2, '0') + ' / ' + String(group.length).padStart(2, '0') + ' · ' + (trigger.closest('.ribbon-group')?.dataset.title || 'Gallery');
    }
    openers.forEach(button => button.addEventListener('click', () => {
        trigger = button; group = [...button.closest('.ribbon-group').querySelectorAll('.gallery-open')];
        lightboxOpen = true; closeMenu(); oldOverflow = document.body.style.overflow; document.body.style.overflow = 'hidden';
        box.showModal(); show(group.indexOf(button)); updateRibbonMedia(); box.querySelector('.lightbox-close').focus();
    }));
    box.querySelector('.lightbox-close').addEventListener('click', () => box.close());
    box.querySelector('.lightbox-prev').addEventListener('click', () => show(index - 1)); box.querySelector('.lightbox-next').addEventListener('click', () => show(index + 1));
    box.addEventListener('keydown', e => { if (e.key === 'ArrowRight' && e.target !== movie) { e.preventDefault(); show(index + 1); } if (e.key === 'ArrowLeft' && e.target !== movie) { e.preventDefault(); show(index - 1); } });
    box.addEventListener('close', () => { movie.pause(); movie.removeAttribute('src'); movie.load(); lightboxOpen = false; document.body.style.overflow = oldOverflow; updateRibbonMedia(); trigger?.focus({ preventScroll: true }); });
    img.addEventListener('load', fit); addEventListener('resize', () => { if (box.open) fit(); });
    let touchX = null; mediaStage.addEventListener('touchstart', e => { if (e.target === movie) return; touchX = e.changedTouches[0].clientX; }, { passive: true }); mediaStage.addEventListener('touchend', e => { if (touchX !== null) { const delta = e.changedTouches[0].clientX - touchX; if (Math.abs(delta) > 55) show(index + (delta < 0 ? 1 : -1)); touchX = null; } }, { passive: true });
}

// Respect a motion preference changed while this page is open.
matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', e => {
    reduced = e.matches;
    if (reduced) { document.querySelectorAll('video').forEach(video => video.pause()); ribbonUserPaused = true; if (motionButton) { motionButton.textContent = 'Play films'; motionButton.setAttribute('aria-pressed', 'true'); } }
    updateRibbonMedia();
});
