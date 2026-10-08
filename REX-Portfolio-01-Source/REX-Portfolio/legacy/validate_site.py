from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json, re, subprocess
R=Path(__file__).parent/'dist'
D=json.loads((R/'content.json').read_text())
BASE='6779074d1142baeb3297de9d04c396077ba87c1d'
PREVIOUS='e935439add0b371ba59b9baa91aadccb84297ba7'
v6=json.loads(subprocess.check_output(['git','show',PREVIOUS+':dist/content.json'],text=True))
v6_projects={p['id']:p for p in v6['projects']}
previous=json.loads(subprocess.check_output(['git','show',BASE+':dist/content.json'],text=True))
old_projects={p['id']:p for p in previous['projects']}
assert [p['id'] for p in D['projects']]==['cambrook','lois-chloe','designora','travel-agencies','food-beverage','sole-frequency']
assert 'supportive-care' not in [p['id'] for p in D['projects']]
assert not (R/'work/supportive-care/index.html').exists()
projects={p['id']:p for p in D['projects']}
lois=projects['lois-chloe']
assert lois['title']=='LOIS CHLOÉ'
assert [a['title'] for a in lois['albums']]==['Lip Oil','Sunscreen','Lipstick']
assert lois['thumbnail']==old_projects['lois-lip-oil']['thumbnail']
assert lois['thumbnail']['type']=='video'
for album in lois['albums']:
 old=old_projects[album['legacy_id']]
 assert album['media']==old['media'],album['id']
 assert album['cover']==old['cover'],album['id']
for p in D['projects']:
 if p['id'] not in ('designora','food-beverage'):assert p==v6_projects[p['id']],p['id']
food=projects['food-beverage']
assert food['title']=='AFTERTASTE'
assert food['category']=='Food & drink visuals'
assert {k:v for k,v in food.items() if k not in ('title','category')}=={k:v for k,v in v6_projects['food-beverage'].items() if k not in ('title','category')}
designora=projects['designora']
assert designora['title']=='DESIGNORA'
assert designora['cover']==v6_projects['designora-01']['cover']
assert [a['id'] for a in designora['albums']]==['project-01','project-02']
assert [a['title'] for a in designora['albums']]==['Project01','Project02']
assert [len(a['media']) for a in designora['albums']]==[5,8]
for album in designora['albums']:
 old=v6_projects[album['legacy_id']]
 assert {k:v for k,v in album.items() if k not in ('id','title','legacy_id')}=={k:v for k,v in old.items() if k not in ('id','title')}
assert sum(len(a['media']) for a in designora['albums'])==13
assert D['photography_albums']==previous['photography_albums']
assert projects['food-beverage']['thumbnail']['source_id']=='1LBp53OTndC1qnj8A6Q3kvIuZIjRPfy25'
assert projects['food-beverage']['thumbnail']['type']=='video'
assert lois['albums'][2]['cover']['rotation']==90
lipstick_stills=[a for a in lois['albums'][2]['media'] if a['type']=='image']
assert [a['src'].split('/')[-1] for a in lipstick_stills[:5]]==[f'drive-{i:02}.webp' for i in range(1,6)]
assert all('/ruby-dance/' in a['src'] for a in lipstick_stills[:5])
assert projects['sole-frequency']['cover']['source_id']=='libfile_a3ecb18e60c0819187d7efd6fa87c270'
assert [len(a['media']) for a in D['photography_albums']]==[17,7]
assert len(D['projects'][-1]['media'])==8
assert sum(bool(a.get('caption')) for a in D['photography_albums'][0]['media'])==4
missing=[]
class References(HTMLParser):
 def handle_starttag(self,t,a):
  if t=='video':
   attrs=dict(a)
   assert all(k in attrs for k in ('autoplay','muted','playsinline')),attrs
  for k,v in a:
   if k in ('src','href','poster','data-full','data-src') and v and v.startswith('/') and not v.startswith('//'):
    path=urlsplit(v).path; f=R/path.lstrip('/');f=f/'index.html' if path.endswith('/') else f
    if not f.exists():missing.append(str(f))
for f in R.rglob('*.html'):References().feed(f.read_text())
assert not missing,missing
for p in D['projects']:
 html=(R/'work'/p['id']/'index.html').read_text()
 groups=p.get('albums',[p])
 assert html.count('class="gallery-open"')==sum(a['type']=='image' for g in groups for a in g['media']),p['id']
 if p.get('albums'):
  for album in p['albums']:
   section=re.search(r'<section class="project-album" id="'+album['id']+r'".*?</section>',html).group()
   assert section.count('class="gallery-open"')==sum(a['type']=='image' for a in album['media'])
   if any(a['type']=='video' for a in album['media']):
    assert section.index('gallery-videos')<section.index('gallery-grid')
    assert section.index('<video')<section.index('<img')
   assert f'href="#{album["id"]}"' in html
   redirect=(R/'work'/album['legacy_id']/'index.html').read_text()
   assert f'content="0; url=/work/{p["id"]}/#{album["id"]}"' in redirect
   assert f'href="/work/{p["id"]}/#{album["id"]}"' in redirect
  if p['id']=='lois-chloe':assert 'class="case-cover rotated-cover"' in html
  assert f'aria-label="{p["title"]} albums"' in html
 else:
  if any(a['type']=='video' for a in p['media']):assert html.index('gallery-videos')<html.index('gallery-grid')
for index in ['index.html','design/index.html','film/index.html','project/index.html']:
 html=(R/index).read_text()
 assert html.count('<h3><span>02.</span> LOIS CHLOÉ</h3>')==1,index
 assert not any(f'href="/work/{old}/"' in html for old in ['lois-lip-oil','lois-sunscreen','lois-lipstick'])
for index in ['index.html','design/index.html','project/index.html']:
 html=(R/index).read_text()
 assert html.count('<h3><span>03.</span> DESIGNORA</h3>')==1,index
 assert not any(f'href="/work/{old}/"' in html for old in ['designora-01','designora-02'])
 assert 'AFTERTASTE</h3>' in html
 assert 'Food &amp; drink visuals' in html
assert 'AFTERTASTE' in (R/'work/food-beverage/index.html').read_text()
assert not any('FOOD &amp; BEVERAGE' in f.read_text() for f in R.rglob('*.html'))
# About is additive: preserve all prior CSS/JS and every pre-existing asset.
V7='e543844caa1cb4faee2efa5bc0960ccdc5aa433a'
for path in ('dist/style.css','dist/app.js'):
 original=subprocess.check_output(['git','show',V7+':'+path],text=True)
 assert Path(path).read_text().startswith(original),path
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',V7,'--','dist/assets'],text=True).splitlines():
 assert Path(path).read_bytes()==subprocess.check_output(['git','show',V7+':'+path]),path
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',V7,'--','dist'],text=True).splitlines():
 if path.endswith('.html') and path!='dist/index.html':
  assert Path(path).read_bytes()==subprocess.check_output(['git','show',V7+':'+path]),path
home=(R/'index.html').read_text()
about=re.search(r'<section id="about".*?</section>',home).group()
assert about.count('id="about-video"')==1
assert '<source data-src="/assets/about/bold-boho-landscape.mp4"' in about
assert 'poster="/assets/about/bold-boho-poster.jpg"' in about
assert 'autoplay muted loop playsinline preload="none"' in about
assert 'aria-controls="about-video"' in about
assert 'prefers-reduced-motion: reduce' in (R/'app.js').read_text()
assert '.about-motion video{visibility:hidden}' in (R/'style.css').read_text()
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(R/'assets/about/bold-boho-landscape.mp4')],text=True))
assert len(info['streams'])==1
video=info['streams'][0]
assert video['codec_name']=='h264' and (video['width'],video['height'])==(1280,720)
assert video['pix_fmt']=='yuv420p' and abs(float(video['duration'])-32)<.05
assert int(info['format']['size'])<8_000_000
assert not any(side.get('rotation',0) for side in video.get('side_data_list',[]))
# Source unchanged, with About content and decorative controls as the only homepage change.
oldhome=subprocess.check_output(['git','show',V7+':dist/index.html'],text=True)
assert re.sub(r'<section id="about".*?</section>','ABOUT',home)==re.sub(r'<section id="about".*?</section>','ABOUT',oldhome)
oldabout=re.search(r'<section id="about".*?</section>',oldhome).group()
assert re.sub(r'<div class="about-motion".*?</div>','BACKGROUND',about).replace('<button class="about-playback" id="about-playback" type="button" aria-controls="about-video" hidden>Pause background</button>','')==re.sub(r'<div class="about-motion".*?</div>','BACKGROUND',oldabout)
print('PASS: 32-second landscape H.264 About background; muted loop, deferred loading, reduced-motion poster and pause control; About copy and navigation preserved; all prior assets, case pages, galleries, data, CSS and JS preserved; all local references resolve.')
