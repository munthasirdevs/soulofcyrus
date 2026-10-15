// AFTR: native horizontal scrolling, independent from the curved galleries.
(() => {
    const rail = document.querySelector('.aftr-rail'); if (!rail) return;
    const panels = [...rail.querySelectorAll('.aftr-panel')], buttons = panels.map(p => p.querySelector('.case-open'));
    const motion = document.querySelector('.case-motion'), prev = document.querySelector('.case-prev'), next = document.querySelector('.case-next'), slider = document.querySelector('.case-range');
    const preference = matchMedia('(prefers-reduced-motion: reduce)');
    let paused = preference.matches, index = 0, modalIndex = 0, returnTarget = null, renderingHistory = false, frame = 0;
    try { paused = paused || sessionStorage.getItem('aftr-film-paused') === 'true'; } catch { }
    const dialog = document.createElement('dialog'); dialog.className = 'lightbox'; dialog.setAttribute('aria-label', 'AFTR artwork full view');
    dialog.innerHTML = '<div class="lightbox-inner"><div class="lightbox-bar"><span class="lightbox-count" aria-live="polite"></span><button class="lightbox-close" type="button" autofocus>[ CLOSE × ]</button></div><div class="lightbox-stage"><button class="lightbox-arrow lightbox-prev" type="button" aria-label="Previous artwork">‹</button><div class="lightbox-media"><img class="lightbox-image" alt=""><video class="lightbox-video" controls muted playsinline preload="metadata" hidden></video></div><button class="lightbox-arrow lightbox-next" type="button" aria-label="Next artwork">›</button></div><p class="lightbox-caption"></p></div>';
    document.body.appendChild(dialog);
    const image = dialog.querySelector('img'), movie = dialog.querySelector('video'), close = dialog.querySelector('.lightbox-close');
    const max = () => Math.max(0, rail.scrollWidth - rail.clientWidth);
    function media() {
        panels.forEach(p => { const v = p.querySelector('video'); if (!v) return; const r = p.getBoundingClientRect(); const visible = r.right > 0 && r.left < rail.clientWidth; if (!paused && !dialog.open && !document.hidden && visible) v.play().catch(() => { }); else v.pause(); });
        motion.textContent = paused ? 'Play film' : 'Pause film'; motion.setAttribute('aria-pressed', String(paused));
    }
    function remember() { try { sessionStorage.setItem('aftr-film-paused', String(paused)); } catch { } }
    function locationFor(i, view = false) { return '#' + panels[i].id + (view ? '/view' : ''); }
    function setLocation(i, view = false, push = false) { if (location.hash === locationFor(i, view)) return; history[push ? 'pushState' : 'replaceState'](view ? { aftrView: true } : null, '', locationFor(i, view)); }
    function nearest() { let best = 0, d = Infinity; panels.forEach((p, i) => { const distance = Math.abs(p.offsetLeft - rail.scrollLeft); if (distance < d) { best = i; d = distance; } }); return best; }
    function update() {
        frame = 0; index = nearest(); const pct = max() ? Math.min(100, Math.max(0, rail.scrollLeft / max() * 100)) : 0;
        document.querySelector('.case-progress').textContent = Math.round(pct) + '%'; slider.value = pct; slider.setAttribute('aria-valuetext', Math.round(pct) + ' percent through AFTR');
        document.querySelector('.case-current').textContent = String(index + 1).padStart(2, '0') + ' / ' + String(panels.length).padStart(2, '0'); document.querySelector('.case-chapter').textContent = panels[index].dataset.chapter;
        prev.disabled = rail.scrollLeft < 2; next.disabled = rail.scrollLeft >= max() - 2;
        if (!dialog.open && !renderingHistory) setLocation(index); media();
    }
    function go(i, push = false) { i = Math.max(0, Math.min(panels.length - 1, i)); if (push) setLocation(i, false, true); rail.scrollTo({ left: panels[i].offsetLeft, behavior: preference.matches || renderingHistory ? 'instant' : 'smooth' }); }
    function show(i) {
        modalIndex = (i + buttons.length) % buttons.length; const b = buttons[modalIndex], isVideo = b.dataset.type === 'video'; movie.pause(); movie.removeAttribute('src'); movie.load(); movie.hidden = !isVideo; image.hidden = isVideo;
        if (isVideo) { movie.src = b.dataset.full; movie.poster = b.querySelector('video').poster; movie.muted = true; if (!paused && !document.hidden) movie.play().catch(() => { }); }
        else { image.src = b.dataset.full; image.alt = b.querySelector('img').alt; }
        dialog.querySelector('.lightbox-caption').textContent = b.dataset.caption; dialog.querySelector('.lightbox-count').textContent = 'AFTR · ' + String(modalIndex + 1).padStart(2, '0') + ' / ' + String(buttons.length).padStart(2, '0');
    }
    function open(i, push = true) { returnTarget = buttons[i]; if (!dialog.open) { closeMenu(); setAbout(false); dialog.showModal(); } show(i); if (push) setLocation(i, true, true); media(); close.focus(); }
    function dismiss() { if (!dialog.open) return; const ownedEntry = history.state?.aftrView; dialog.close(); if (ownedEntry) history.back(); else { setLocation(modalIndex); rail.scrollTo({ left: panels[modalIndex].offsetLeft, behavior: 'instant' }); } }
    function readLocation() { let id; try { id = decodeURIComponent(location.hash.slice(1)); } catch { id = ''; } const view = id.endsWith('/view'); if (view) id = id.slice(0, -5); const i = Math.max(0, panels.findIndex(p => p.id === id)); renderingHistory = true; if (view) open(i, false); else if (dialog.open) dialog.close(); rail.scrollTo({ left: panels[i].offsetLeft, behavior: 'instant' }); update(); renderingHistory = false; }
    buttons.forEach((b, i) => b.addEventListener('click', () => open(i)));
    close.addEventListener('click', dismiss); dialog.addEventListener('cancel', e => { e.preventDefault(); dismiss(); });
    dialog.addEventListener('close', () => { movie.pause(); movie.removeAttribute('src'); movie.load(); media(); returnTarget?.focus({ preventScroll: true }); });
    function modalMove(step) { show(modalIndex + step); history.replaceState(history.state, '', locationFor(modalIndex, true)); }
    dialog.querySelector('.lightbox-prev').addEventListener('click', () => modalMove(-1)); dialog.querySelector('.lightbox-next').addEventListener('click', () => modalMove(1));
    dialog.addEventListener('keydown', e => { if (e.target === movie) return; if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); modalMove(e.key === 'ArrowRight' ? 1 : -1); } });
    rail.addEventListener('scroll', () => { if (!frame) frame = requestAnimationFrame(update); }, { passive: true });
    // Listen across the page: the fixed dock and header are siblings of the rail.
    // Keep zoom, form controls and open information/navigation independently usable.
    document.addEventListener('wheel', e => {
        if (e.ctrlKey || dialog.open || document.querySelector('.site-menu:not([hidden])')) return;
        if (e.target.closest?.('input,textarea,select,[contenteditable="true"],.project-dock.expanded')) return;
        const delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
        if (!delta || !max()) return;
        e.preventDefault();
        const unit = e.deltaMode === 1 ? 18 : e.deltaMode === 2 ? rail.clientWidth : 1;
        rail.scrollTo({ left: Math.max(0, Math.min(max(), rail.scrollLeft + delta * unit)), behavior: 'instant' });
    }, { passive: false });
    rail.addEventListener('keydown', e => { if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); go(nearest() + (e.key === 'ArrowRight' ? 1 : -1), true); } if (e.key === 'Home' || e.key === 'End') { e.preventDefault(); go(e.key === 'Home' ? 0 : panels.length - 1, true); } });
    prev.addEventListener('click', () => go(nearest() - 1, true)); next.addEventListener('click', () => go(nearest() + 1, true)); slider.addEventListener('input', () => rail.scrollTo({ left: Number(slider.value) / 100 * max(), behavior: 'instant' }));
    motion.hidden = !rail.querySelector('video'); motion.addEventListener('click', () => { paused = !paused; remember(); media(); });
    preference.addEventListener('change', e => { if (e.matches) { paused = true; movie.pause(); remember(); } media(); }); document.addEventListener('visibilitychange', () => { if (document.hidden) movie.pause(); media(); });
    addEventListener('popstate', readLocation); addEventListener('hashchange', readLocation); addEventListener('resize', () => { if (!dialog.open) { renderingHistory = true; go(index); requestAnimationFrame(() => { update(); renderingHistory = false; }); } });
    readLocation();
})();
