// Dependency-free cursor lifecycle regression checks. This simulated DOM does
// not establish visual contrast, CSS stacking, or real browser pointer behavior.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const source = fs.readFileSync(path.join(__dirname, 'dist/cursor.js'), 'utf8');

function setup(options = {}) {
  class Events {
    constructor() { this.events = new Map(); }
    addEventListener(type, listener) {
      const listeners = this.events.get(type) || [];
      listeners.push(listener);
      this.events.set(type, listeners);
    }
    fire(type, values = {}) {
      const event = { target: this, ...values };
      for (const listener of this.events.get(type) || []) listener(event);
    }
  }
  class Element extends Events {
    constructor(tag = 'div', attrs = {}) {
      super();
      this.tagName = tag.toUpperCase();
      this.attrs = { ...attrs };
      this.children = [];
      this.parentElement = null;
      this.dataset = {};
      this.style = {};
      this.textContent = '';
      this.classes = new Set();
      this.classList = {
        add: (...names) => names.forEach(name => this.classes.add(name)),
        remove: (...names) => names.forEach(name => this.classes.delete(name)),
        contains: name => this.classes.has(name),
        toggle: (name, force) => {
          const add = force === undefined ? !this.classes.has(name) : force;
          if (add) this.classes.add(name); else this.classes.delete(name);
          return add;
        }
      };
      if (attrs.class) this.className = attrs.class;
    }
    set className(value) { this.classes = new Set(value.split(/\s+/).filter(Boolean)); }
    get className() { return [...this.classes].join(' '); }
    setAttribute(name, value) { this.attrs[name] = value; }
    appendChild(child) { child.parentElement = this; this.children.push(child); return child; }
    matches(selector) {
      if (selector === ':disabled') return Object.hasOwn(this.attrs, 'disabled');
      const tag = selector.match(/^[a-z]+/i)?.[0];
      if (tag && this.tagName !== tag.toUpperCase()) return false;
      for (const name of selector.matchAll(/\.([\w-]+)/g)) {
        if (!this.classes.has(name[1])) return false;
      }
      for (const attr of selector.matchAll(/\[([\w-]+)(?:="([^"]*)")?\]/g)) {
        if (!Object.hasOwn(this.attrs, attr[1])) return false;
        if (attr[2] !== undefined && this.attrs[attr[1]] !== attr[2]) return false;
      }
      return Boolean(tag || selector.startsWith('.') || selector.startsWith('['));
    }
    closest(selectors) {
      for (let element = this; element; element = element.parentElement) {
        if (selectors.split(',').some(selector => element.matches(selector.trim()))) return element;
      }
      return null;
    }
  }
  const document = new Events();
  document.hidden = false;
  document.documentElement = new Element('html');
  document.body = document.documentElement.appendChild(new Element('body'));
  document.createElement = tag => new Element(tag);
  const visit = (element, selector) => element.matches(selector) ? element :
    element.children.map(child => visit(child, selector)).find(Boolean) || null;
  document.querySelector = selector => visit(document.documentElement, selector);
  let hit = document.body, hitTests = 0, ready = options.ready ?? true;
  document.elementFromPoint = () => { hitTests++; return hit; };
  const window = new Events();
  window.PointerEvent = options.pointerEvent === false ? undefined : function PointerEvent() {};
  const CSS = { supports: (property) => property.startsWith('selector') ?
    options.hasSelector !== false : options.blend !== false };
  window.CSS = options.css === false ? undefined : CSS;
  const preference = new Events();
  preference.matches = options.matches ?? true;
  const frames = new Map(), observers = [];
  let nextFrame = 0, frameRequests = 0;
  class MutationObserver {
    constructor(listener) { this.listener = listener; }
    observe(target, config) { observers.push({ listener: this.listener, target, config }); }
  }
  const context = {
    window, document, Element, CSS, MutationObserver,
    matchMedia: query => { preference.query = query; return preference; },
    getComputedStyle: () => ({ getPropertyValue: () => ready ? '1' : '' }),
    requestAnimationFrame: fn => { frameRequests++; frames.set(++nextFrame, fn); return nextFrame; },
    cancelAnimationFrame: id => frames.delete(id)
  };
  vm.runInNewContext(source, context, { filename: 'cursor.js' });
  const cursor = document.querySelector('.rex-cursor');
  const root = document.documentElement;
  const flush = () => {
    let runs = 0;
    while (frames.size) {
      assert(++runs < 20, 'Cursor must not run an unbounded idle animation loop');
      const pending = [...frames.values()]; frames.clear();
      pending.forEach(fn => fn());
    }
  };
  const mouse = (type, target = document.body, extra = {}) => document.fire(type, {
    pointerType: 'mouse', target, clientX: 140, clientY: 90, button: 0, ...extra
  });
  const move = (target = document.body, extra = {}) => { mouse('pointermove', target, extra); flush(); };
  return {
    document, window, preference, root, cursor, Element, frames, observers,
    flush, mouse, move, active: () => root.classList.contains('rex-cursor-active'),
    add: (tag, attrs, parent = document.body) => parent.appendChild(new Element(tag, attrs)),
    setHit: target => { hit = target; },
    setReady: value => { ready = value; },
    mutations: () => observers.forEach(observer => observer.listener([])),
    frameRequests: () => frameRequests, hitTests: () => hitTests
  };
}

let passed = 0;
function test(name, run) { run(); passed++; console.log('PASS cursor: ' + name); }

test('capability and preference gates retain native cursor', () => {
  for (const options of [{ pointerEvent: false }, { css: false }, { blend: false }, { hasSelector: false }]) {
    const h = setup(options); h.move(); assert(!h.cursor); assert(!h.active());
  }
  const h = setup({ matches: false });
  h.move(); assert(!h.active()); assert.equal(h.frames.size, 0);
  assert(h.preference.query.includes('hover: hover'));
  assert(h.preference.query.includes('pointer: fine'));
  assert(h.preference.query.includes('prefers-reduced-motion: no-preference'));
  assert(h.preference.query.includes('forced-colors: none'));
});

test('first movement activates; frames coalesce and stop at idle', () => {
  const h = setup();
  assert(!h.active()); assert.equal(h.cursor.attrs['aria-hidden'], 'true');
  h.mouse('pointerover'); h.mouse('pointerdown'); h.mouse('pointerup');
  assert.equal(h.frames.size, 0); assert(!h.active());
  for (let i = 0; i < 10; i++) h.mouse('pointermove', h.document.body, { clientX: i, clientY: 17 });
  assert.equal(h.frames.size, 1); assert.equal(h.frameRequests(), 1);
  h.flush(); assert(h.active());
  assert.equal(h.cursor.style.transform, 'translate3d(9px, 17px, 0)');
  assert.equal(h.frames.size, 0); assert.equal(h.frameRequests(), 1);
  h.flush(); assert.equal(h.frameRequests(), 1);
});

test('view, link, default and pressed states follow actual targets', () => {
  const h = setup();
  const link = h.add('a', { href: '/' }), child = h.add('span', {}, link);
  h.move(child); assert.equal(h.cursor.dataset.state, 'link');
  h.mouse('pointerdown', child); h.flush(); assert(h.cursor.classList.contains('is-pressed'));
  h.setHit(child); h.mouse('pointerup', child); h.flush(); assert(!h.cursor.classList.contains('is-pressed'));
  const card = h.add('button', { class: 'gallery-open' });
  h.move(card); assert.equal(h.cursor.dataset.state, 'view');
  assert.equal(h.cursor.children[0].textContent, 'View');
  h.move(); assert.equal(h.cursor.dataset.state, 'default');
});

test('native controls and descendants restore native cursor immediately', () => {
  const h = setup();
  const cases = [
    ['input', { type: 'range' }], ['input', { type: 'text' }], ['textarea', {}], ['select', {}],
    ['video', { controls: '' }], ['iframe', {}], ['div', { contenteditable: 'true' }],
    ['div', { 'data-native-cursor': '' }], ['button', { disabled: '' }], ['button', { 'aria-disabled': 'true' }]
  ];
  for (const [tag, attrs] of cases) {
    h.move(); assert(h.active());
    const target = h.add(tag, attrs), child = h.add('span', {}, target);
    h.mouse('pointerover', child); assert(!h.active(), tag + ' must not wait for rAF');
    h.flush(); assert(!h.active());
    h.move(target); assert(!h.active());
  }
  h.move(); assert(h.active()); assert.equal(h.frames.size, 0);
});

test('dialog opening resets; closing requires fresh mouse movement', () => {
  const h = setup(); h.move(); assert(h.active());
  h.mouse('pointermove'); assert.equal(h.frames.size, 1);
  const dialog = h.add('dialog', { open: '' }); h.mutations();
  assert(!h.active()); assert.equal(h.frames.size, 0);
  h.move(dialog); assert(!h.active());
  delete dialog.attrs.open; h.mutations();
  h.mouse('pointerover'); h.mouse('pointerup'); h.flush(); assert(!h.active());
  h.move(); assert(h.active());
});

test('captured gallery drag takes priority and release rechecks actual target', () => {
  const h = setup();
  const stage = h.add('div', { class: 'ribbon-stage' });
  const card = h.add('button', { class: 'gallery-open' }, stage);
  const link = h.add('a', { href: '/' });
  h.move(card); assert.equal(h.cursor.dataset.state, 'view');
  h.mouse('pointerdown', card); stage.classList.add('dragging');
  h.move(stage); assert.equal(h.cursor.dataset.state, 'drag');
  assert(h.cursor.classList.contains('is-pressed'));
  stage.classList.remove('dragging'); h.setHit(link);
  h.mouse('pointerup', stage); h.mouse('lostpointercapture', stage); h.flush();
  assert.equal(h.cursor.dataset.state, 'link'); assert.equal(h.hitTests(), 1);
  assert(!h.cursor.classList.contains('is-pressed'));
  h.move(stage); assert.equal(h.cursor.dataset.state, 'drag');
  h.document.fire('pointercancel'); assert(!h.active()); assert.equal(h.frames.size, 0);
});

test('keyboard, blur, hidden page, touch, pen and pointer exit cancel pending frames', () => {
  const resets = [
    h => h.document.fire('keydown', { key: 'Tab' }),
    h => h.window.fire('blur'),
    h => h.window.fire('pagehide'),
    h => h.document.fire('visibilitychange'),
    h => h.document.fire('contextmenu'),
    h => h.root.fire('pointerleave'),
    h => h.mouse('pointermove', h.document.body, { pointerType: 'touch' }),
    h => h.mouse('pointerover', h.document.body, { pointerType: 'pen' }),
    h => h.mouse('pointerdown', h.document.body, { pointerType: 'touch' })
  ];
  for (const reset of resets) {
    const h = setup(); h.move(); h.mouse('pointermove');
    assert(h.active()); assert.equal(h.frames.size, 1);
    reset(h); assert(!h.active()); assert.equal(h.frames.size, 0);
    h.mouse('pointerover'); h.mouse('pointerup'); h.flush(); assert(!h.active());
    h.move(); assert(h.active());
  }
  const h = setup(); h.move(); h.document.hidden = true; h.mouse('pointermove'); h.flush();
  assert(!h.active());
});

test('media preference changes never resurrect stale cursor position', () => {
  const h = setup(); h.move(); h.mouse('pointermove');
  h.preference.matches = false; h.preference.fire('change');
  assert(!h.active()); assert.equal(h.frames.size, 0);
  h.move(); assert(!h.active());
  h.preference.matches = true; h.preference.fire('change'); h.flush(); assert(!h.active());
  h.move(); assert(h.active());
});

test('missing stylesheet fails safely and later loading permits activation', () => {
  const h = setup({ ready: false }); h.move();
  assert(!h.active()); assert.equal(h.frames.size, 0);
  h.setReady(true); h.mouse('pointerover'); h.flush(); assert(!h.active());
  h.move(); assert(h.active());
  h.setReady(false); h.mouse('pointermove'); h.flush(); assert(!h.active());
});

test('scroll and resize recheck hover once without autonomous animation', () => {
  const h = setup(); h.move();
  const input = h.add('input', { type: 'range' }); h.setHit(input);
  h.document.fire('scroll'); h.window.fire('resize');
  assert.equal(h.frames.size, 1); h.flush(); assert(!h.active()); assert.equal(h.hitTests(), 1);
  h.setHit(h.document.body); h.document.fire('scroll'); h.flush();
  assert(h.active()); assert.equal(h.frames.size, 0);
});

console.log(`PASS: ${passed} cursor simulated-DOM regression groups. Native browser visual, CSS and pointer QA remain separate.`);
