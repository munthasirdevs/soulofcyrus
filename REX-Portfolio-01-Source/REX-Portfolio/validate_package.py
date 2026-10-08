#!/usr/bin/env python3
"""Read-only static checks for this standalone portfolio; Python stdlib only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent / 'dist'
errors = []
external = set()
documents = {}
references = []


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                errors.append(f'{self.path.relative_to(ROOT)}: duplicate ID {attrs["id"]}')
            self.ids.add(attrs['id'])
        for key in ('src', 'href', 'poster', 'data-full', 'data-src'):
            if attrs.get(key):
                references.append((self.path, attrs[key]))
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            match = re.search(r'url=(.*)', attrs.get('content', ''), re.I)
            if match:
                references.append((self.path, match.group(1)))


def check_reference(origin, value):
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme in ('http', 'https') or parsed.netloc:
            external.add(value)
        return
    path = unquote(parsed.path)
    target = ((ROOT / path.lstrip('/')) if path.startswith('/') else
              (origin.parent / path if path else origin)).resolve()
    if not target.is_relative_to(ROOT):
        errors.append(f'{origin.relative_to(ROOT)}: path escapes web root: {value}')
        return
    if target.is_dir():
        target /= 'index.html'
    if not target.is_file():
        errors.append(f'{origin.relative_to(ROOT)}: missing {value}')
    elif parsed.fragment and target.suffix == '.html':
        page = documents.get(target)
        if page and unquote(parsed.fragment) not in page.ids:
            errors.append(f'{origin.relative_to(ROOT)}: missing anchor {value}')


def data_references(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in ('src', 'poster', 'portrait', 'aboutVideo') and isinstance(item, str):
                references.append((ROOT / 'content.json', item))
            data_references(item)
    elif isinstance(value, list):
        for item in value:
            data_references(item)


if not (ROOT / 'index.html').is_file():
    sys.exit('FAIL: dist/index.html is missing. Run from the complete extracted archive.')
for path in sorted(ROOT.rglob('*.html')):
    page = Page(path)
    page.feed(path.read_text(encoding='utf-8'))
    documents[path] = page
for path in ROOT.rglob('*.css'):
    for match in re.finditer(r'url\(\s*[\'\"]?([^\'\"\)\s]+)', path.read_text(encoding='utf-8')):
        references.append((path, match.group(1)))
data = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
data_references(data)
for origin, value in references:
    check_reference(origin, value)
node = shutil.which('node')
if node:
    for path in ROOT.rglob('*.js'):
        result = subprocess.run([node, '--check', str(path)], capture_output=True, text=True)
        if result.returncode:
            errors.append(f'{path.name}: JavaScript syntax failed: {result.stderr.strip()}')
if errors:
    print('\n'.join('FAIL: ' + error for error in errors))
    sys.exit(1)
images = sum(path.suffix.lower() in ('.webp', '.jpg', '.jpeg', '.png') for path in ROOT.rglob('*'))
videos = len(list(ROOT.rglob('*.mp4')))
print(f'PASS: {len(documents)} HTML pages; {len(references)} local/external references inspected; local file references and anchors resolve.')
print(f'Inventory: {images} images, {videos} videos, {len(data.get("projects", []))} main projects.')
print('JavaScript syntax: ' + ('PASS' if node else 'NOT RUN (Node is optional and not installed).'))
print('External references are preserved but not requested or checked. Media decode and interactive browser QA are outside this validator.')
