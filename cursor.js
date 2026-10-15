// Independent pointer enhancement; gallery drag, clicks and focus remain native.
(() => {
  if (!window.PointerEvent || !window.CSS?.supports('mix-blend-mode', 'difference') ||
    !CSS.supports('selector(:has(*))')) return;

  const preference = matchMedia('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference) and (forced-colors: none)');
  const root = document.documentElement;
  const cursor = document.createElement('div');
  cursor.className = 'rex-cursor';
  cursor.setAttribute('aria-hidden', 'true');
  const shape = document.createElement('span');
  shape.className = 'rex-cursor-shape';
  cursor.appendChild(shape);
  document.body.appendChild(cursor);

  const nativeTargets = 'input, textarea, select, [contenteditable], video[controls], iframe, [data-native-cursor], :disabled, [aria-disabled="true"]';
  const viewTargets = '.gallery-open, .case-open, .work-visual';
  const linkTargets = 'a[href], button, [role="button"], summary';
  let frame = 0, tracking = false, pressed = false, target = null;
  let x = 0, y = 0, hitTest = false;

  function hide() {
    root.classList.remove('rex-cursor-active');
    cursor.classList.remove('is-pressed');
  }

  function reset() {
    tracking = false;
    pressed = false;
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    hide();
  }

  function render() {
    frame = 0;
    if (!tracking || !preference.matches || document.hidden ||
      document.querySelector('dialog[open]') ||
      getComputedStyle(cursor).getPropertyValue('--rex-cursor-ready').trim() !== '1') {
      reset();
      return;
    }
    if (hitTest) {
      target = document.elementFromPoint(x, y);
      hitTest = false;
    }
    if (!(target instanceof Element) || target.closest(nativeTargets)) {
      hide();
      return;
    }

    // Pointer capture retargets moves to the stage while the gallery drags.
    const dragging = document.querySelector('.ribbon-stage.dragging');
    const state = dragging || target.closest('.ribbon-stage') && !target.closest(viewTargets)
      ? 'drag' : target.closest(viewTargets) ? 'view' : target.closest(linkTargets) ? 'link' : 'default';
    if (cursor.dataset.state !== state) {
      cursor.dataset.state = state;
      shape.textContent = state === 'view' ? 'View' : state === 'drag' ? '↔ Drag' : '';
    }
    cursor.classList.toggle('is-pressed', pressed);
    cursor.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    root.classList.add('rex-cursor-active');
  }

  function schedule(recheck = false) {
    hitTest = hitTest || recheck;
    if (tracking && !frame) frame = requestAnimationFrame(render);
  }

  document.addEventListener('pointermove', event => {
    if (event.pointerType !== 'mouse' || !preference.matches) { reset(); return; }
    tracking = true;
    x = event.clientX;
    y = event.clientY;
    target = event.target;
    schedule();
  }, { passive: true });

  document.addEventListener('pointerover', event => {
    if (event.pointerType !== 'mouse') { reset(); return; }
    target = event.target;
    // Restore native form/media controls before the next animation frame.
    if (target instanceof Element && target.closest(nativeTargets)) hide();
    schedule();
  }, { passive: true });

  document.addEventListener('pointerdown', event => {
    if (event.pointerType !== 'mouse') { reset(); return; }
    pressed = event.button === 0;
    schedule();
  }, { passive: true });
  document.addEventListener('pointerup', () => { pressed = false; schedule(true); }, { passive: true });
  document.addEventListener('lostpointercapture', () => { pressed = false; schedule(true); }, { passive: true });
  document.addEventListener('pointercancel', reset, { passive: true });
  document.documentElement.addEventListener('pointerleave', reset, { passive: true });
  document.addEventListener('keydown', reset);
  document.addEventListener('contextmenu', reset);
  document.addEventListener('visibilitychange', reset);
  window.addEventListener('blur', reset);
  window.addEventListener('pagehide', reset);
  window.addEventListener('resize', () => schedule(true), { passive: true });
  document.addEventListener('scroll', () => schedule(true), { capture: true, passive: true });
  preference.addEventListener('change', reset);

  // Modal viewers use native controls in the top layer. Closing them waits for
  // fresh mouse movement so keyboard focus never revives a stale cursor.
  new MutationObserver(() => {
    if (document.querySelector('dialog[open]')) reset();
  }).observe(document.body, { subtree: true, childList: true, attributes: true, attributeFilter: ['open'] });
})();
