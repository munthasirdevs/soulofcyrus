from pathlib import Path
from html import escape as E
import json
ROOT=Path(__file__).parent/'dist'
DATA=json.loads((ROOT/'content.json').read_text())
PROJECTS=DATA.get('projects',[])
ICON="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23101010'/%3E%3Ctext x='10' y='49' fill='white' font-size='48' font-family='Arial' font-weight='bold'%3ER%3C/text%3E%3C/svg%3E"
def head(title):return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101010"><meta name="description" content="Cyrus Rex. Creative/Art Director. Designer. Design, Film, Photography and SFX/VFX. Based in Dhaka and Athens."><title>{E(title)} — CYRUS REX</title><link rel="stylesheet" href="/style.css"><link rel="icon" href="{ICON}"><link rel="preload" href="/assets/fonts/instrument-serif-italic.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/archivo-variable.woff2" as="font" type="font/woff2" crossorigin></head>'''
def header():return '''<a class="skip" href="#main">Skip to content</a><header><a class="wordmark" href="/" aria-label="Rex home">REX<span>©</span></a><p class="header-location">Based in<br>Dhaka & Athens</p><nav aria-label="Main navigation"><a href="/#work">Work</a><a href="/#about">About</a><a href="/#contact">Contact</a></nav></header>'''
def footer():return '''<footer id="contact" class="pad"><div class="folio"><span>LET’S MAKE SOMETHING</span><span>CYRUS REX</span></div><a class="contact-title pairing" href="mailto:rex.studio.bd@gmail.com"><span>I got the ingredients,</span><strong>LET’S COOK.</strong></a><div class="social-links"><a href="mailto:rex.studio.bd@gmail.com">Mail<small>rex.studio.bd@gmail.com</small></a><a href="https://www.instagram.com/soulofcyrus/" target="_blank" rel="noopener noreferrer">Instagram<small>@soulofcyrus</small></a><a href="https://wa.me/8801938466771" target="_blank" rel="noopener noreferrer">WhatsApp<small>+880 1938466771</small></a></div><div class="footer-base"><span>© 2026 CYRUS REX</span><span>DESIGN / FILM / PHOTOGRAPHY / SFX & VFX</span><a href="#top">Back to top</a></div></footer>'''
def folio(n):return f'<div class="folio case-folio"><span>{n}</span><span>CREATIVE/ART DIRECTOR. DESIGNER</span><a href="mailto:rex.studio.bd@gmail.com">rex.studio.bd@gmail.com</a><span>© 2026</span></div>'
def picture(a,cls='',lazy=True):return f'<img class="{cls}" src="{E(a["src"])}" alt="{E(a.get("alt","Project visual"))}"'+(' loading="lazy"' if lazy else ' fetchpriority="high"')+(f' width="{a["width"]}" height="{a["height"]}"' if a.get('width') else '')+'>'
def media(a,cls=''):
 if a['type']=='video':return f'<video class="{cls}" autoplay muted '+('loop ' if a.get('loop') else '')+f'controls playsinline preload="metadata" poster="{E(a.get("poster",""))}" aria-label="{E(a.get("alt","Project film"))}"><source src="{E(a["src"])}" type="video/mp4"></video>'
 return picture(a,cls)
def cover(a):
 if a.get('rotation')==90:
  ratio=a['width']/a['height']
  return f'<div class="case-cover rotated-cover" style="aspect-ratio:{a["height"]}/{a["width"]};--rotated-width:{100*ratio:.6f}%;--rotated-height:{100/ratio:.6f}%">'+picture(a,lazy=False)+'</div>'
 return picture(a,'case-cover',False)
def thumbnail(a):
 if a['type']=='video':return f'<video class="thumbnail-video" autoplay muted loop playsinline preload="metadata" poster="{E(a.get("poster",""))}" aria-label="{E(a.get("alt","Project film"))}"><source src="{E(a["src"])}" type="video/mp4"></video><span class="thumbnail-badge">FILM</span>'
 return picture(a)
def gallery(assets,opening=None):
 videos=[a for a in assets if a['type']=='video']; images=[a for a in assets if a['type']!='video']
 result='<div class="gallery-videos">'+''.join('<figure class="gallery-video">'+media(a)+'</figure>' for a in videos)+'</div>' if videos else ''
 if opening:result+='<figure class="album-opening">'+cover(opening)+'</figure>'
 result+='<div class="gallery-grid">'
 for a in images:
  result+='<figure class="gallery-item"><button type="button" class="gallery-open" data-full="'+E(a['src'])+'" data-caption="'+E(a.get('caption',a.get('alt','')))+'" aria-label="Enlarge '+E(a.get('alt','image'))+'">'+picture(a)+'<span class="enlarge" aria-hidden="true">↗</span></button>'+(f'<figcaption>{E(a["caption"])}</figcaption>' if a.get('caption') else '')+'</figure>'
 return result+'</div>'
def rows(projects):
 out=''
 for p in projects:
  idx=PROJECTS.index(p)+1
  out+=f'''<article class="work-row"><a class="work-visual" href="/work/{p['id']}/" style="--image-bg:{p.get('color','#181818')}">{thumbnail(p.get('thumbnail',p['cover']))}</a><div class="work-copy"><p class="category">{E(p['category'])}</p><h3><span>{idx:02}.</span> {E(p['title'])}</h3><a class="case-link" href="/work/{p['id']}/">View case<span class="link-circle" aria-hidden="true">+</span></a></div></article>'''
 return out
homepage=head('Selected Work')+'<body id="top">'+header()+'''<main id="main"><section class="hero" aria-label="Introduction"><video id="hero-video" autoplay muted loop playsinline preload="metadata" poster="/assets/hero-poster.jpg"><source src="/assets/hero.mp4" type="video/mp4"></video><div class="hero-overlay"></div><div class="hero-top"><span>DESIGN / FILM / PHOTOGRAPHY / SFX & VFX</span><span>PORTFOLIO — 2026</span></div><p class="hero-role">Creative/Art Director.<br>Designer</p><h1 class="hero-name pairing"><span>CYRUS</span><strong>REX</strong></h1><div class="hero-controls"><button id="sound" aria-pressed="false" type="button">Sound off</button><button id="play" type="button">Pause</button></div></section><section id="intro" class="intro pad"><div class="folio"><span>0.1 / THE PRACTICE</span><span>CYRUS REX</span></div><div class="intro-grid"><figure class="portrait"><img src="/assets/portrait/cyrus-rex-extended.webp" alt="Portrait of Cyrus Rex in a black coat and sunglasses" width="1122" height="1402" loading="lazy"><figcaption>CYRUS REX / CREATIVE PRACTICE</figcaption></figure><div class="intro-copy"><h2 class="pairing"><span>A visual world<br>built on</span><strong>INSTINCT.</strong></h2><p>I’m Cyrus Rex, a creative/art director and designer. My practice moves across <b>Design, Film, Photography and SFX/VFX.</b></p><div class="practice-tags"><span>01 / DESIGN</span><span>02 / FILM</span><span>03 / PHOTOGRAPHY</span><span>04 / SFX/VFX</span></div></div></div></section><section id="work" class="work pad"><div class="folio"><span>0.2 / SELECTED WORK</span><span>AN INDEX OF IDEAS</span></div><div class="work-heading"><h2 class="pairing"><span>Selected</span><strong>WORK.</strong></h2><p>DESIGN / MOVING IMAGE<br>'''+f'{len(PROJECTS):02} PROJECT STORIES'+'''</p></div>'''+rows(PROJECTS)+'''</section><section id="about" class="about pad"><div class="about-motion" aria-hidden="true"><video id="about-video" autoplay muted loop playsinline preload="none" poster="/assets/about/bold-boho-poster.jpg" tabindex="-1"><source data-src="/assets/about/bold-boho-landscape.mp4" type="video/mp4"></video></div><div class="folio"><span>0.3 / BEHIND THE WORK</span><span>FOUR CONNECTED DISCIPLINES</span></div><h2 class="pairing"><span>An eye for detail.<br>A feel for</span><strong>THE UNEXPECTED.</strong></h2><div class="about-bottom"><p>I’m a creative/art director and designer based in Dhaka and Athens. I work across design, film, photography and SFX/VFX, shaping ideas from the first visual thought to the final frame.</p><nav class="disciplines" aria-label="Explore disciplines">'''+''.join(f'<a href="/{slug}/"><small>{i:02}</small>{label}<small>Explore</small></a>' for i,(slug,label) in enumerate([('design','Design'),('film','Film'),('photography','Photography'),('sfx-vfx','SFX/VFX')],1))+'''</nav></div><button class="about-playback" id="about-playback" type="button" aria-controls="about-video" hidden>Pause background</button></section></main>'''+footer()+'<script src="/app.js"></script></body></html>'
(ROOT/'index.html').write_text(homepage)
for i,p in enumerate(PROJECTS):
 path=ROOT/'work'/p['id'];path.mkdir(parents=True,exist_ok=True)
 if p.get('albums'):
  html=head(p['title'])+'<body class="case-page album-case" id="top">'+header()+f'<main id="main" class="case-main pad"><div class="folio"><span>CASE / {i+1:02}</span><a href="/#work">Selected work</a></div><p class="category">{E(p["category"])}</p><h1 class="case-title">{E(p["title"])}</h1><p class="album-case-intro">{E(p["intro"])}</p>'
  html+=f'<nav class="album-nav" aria-label="{E(p["title"])} albums">'+''.join(f'<a href="#{a["id"]}"><span>{j:02}</span>{E(a["title"])}</a>' for j,a in enumerate(p['albums'],1))+'</nav>'
  for j,a in enumerate(p['albums'],1):
   html+=f'<section class="project-album" id="{a["id"]}" aria-labelledby="{a["id"]}-title"><div class="album-heading"><p class="album-number">ALBUM / {j:02}</p><h2 id="{a["id"]}-title">{E(a["title"])}</h2><p>{E(a["intro"])}</p></div>'+gallery(a['media'],a['cover'] if a['cover'].get('rotation') else None)+'</section>'
   legacy=ROOT/'work'/a['legacy_id'];legacy.mkdir(parents=True,exist_ok=True)
   target=f'/work/{p["id"]}/#{a["id"]}'
   redirect=head(f'{p["title"]} / {a["title"]}').replace('</head>',f'<meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="/work/{p["id"]}/"></head>')
   (legacy/'index.html').write_text(redirect+'<body id="top">'+header()+f'<main id="main" class="pad"><h1 class="index-title">{E(a["title"])}</h1><p>This album is now part of {E(p["title"])}.</p><a class="case-link" href="{target}">Open the {E(a["title"])} album</a></main>'+footer()+'</body></html>')
 else:
  html=head(p['title'])+'<body class="case-page" id="top">'+header()+f'<main id="main" class="case-main pad"><h1 class="case-number">Case:{i+1:02}</h1>'+cover(p['cover'])+folio('0.1')+f'<p class="category">{E(p["category"])}</p><h2 class="case-title">{E(p["headline"])}</h2>'+folio('0.2')+f'<p class="case-intro">{E(p["intro"])}</p>'
  if p.get('context'):html+='<p class="brand-context">'+E(p['context'])+(f' <a href="{p["source"]}" target="_blank" rel="noopener noreferrer">Brand background</a>' if p.get('source') else '')+'</p>'
  html+='<dl class="case-facts">'+''.join(f'<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for k,v in [('Project',p['title']),('Format',p['format']),('Focus',p['focus'])])+'</dl>'+folio('0.3')+gallery(p['media'])
 html+=folio('0.4')+'<section class="next-case"><p>Keep exploring</p><h2>Pick another case</h2><div>'
 for k,label in [((i-1)%len(PROJECTS),'Previous'),((i+1)%len(PROJECTS),'Next')]:
  q=PROJECTS[k];html+=f'<a href="/work/{q["id"]}/"><small>{label}</small>{E(q["title"])}</a>'
 html+='</div></section></main>'+footer()+'<script src="/app.js"></script></body></html>'
 (path/'index.html').write_text(html)
for n,(slug,title,tag,desc) in enumerate([('design','Design','Ideas, made visible.','Visual identities, campaign imagery and editorial design.'),('film','Film','Stories in motion.','Product films, moving-image studies and campaign visuals.'),('photography','Photography','Light. Form. Feeling.','Photography, personal studies and photo editing.'),('sfx-vfx','SFX/VFX','Beyond the frame.','A dedicated space for sound and visual effects.')],1):
 selected=[p for p in PROJECTS if slug in p['disciplines']]
 main=f'<main id="main"><section class="discipline-hero pad"><div class="folio"><span>DISCIPLINE / {n:02}</span><a href="/#about">All disciplines</a></div><h1>{title}</h1><div class="discipline-desc"><h2>{tag}</h2><p>{desc}</p></div></section><section class="discipline-work pad">'+rows(selected)
 if slug=='photography':
  for album in DATA.get('photography_albums',[]):
   main+=f'<section class="photo-album" id="{album["id"]}"><div class="album-heading"><h2>{E(album["title"])}</h2><p>{E(album["intro"])}</p></div>'+gallery(album['media'])+'</section>'
 if not selected and slug!='photography':main+='<div class="empty-selection"><p>Selected work coming soon.</p><a href="/#work">Explore the current work index</a></div>'
 main+='</section><nav class="discipline-nav pad" aria-label="Other disciplines">'+''.join(f'<a href="/{s}/"'+(' aria-current="page"' if s==slug else '')+f'>{t}</a>' for s,t in [('design','Design'),('film','Film'),('photography','Photography'),('sfx-vfx','SFX/VFX')])+'</nav></main>'
 (ROOT/slug/'index.html').write_text(head(title)+f'<body id="top" class="discipline-page">'+header()+main+footer()+'<script src="/app.js"></script></body></html>')
# Preserve the previously published generic case URL as a usable work-index landing.
(ROOT/'project'/'index.html').write_text(head('Work Index')+'<body id="top">'+header()+'<main id="main" class="pad"><h1 class="index-title">Selected work</h1>'+rows(PROJECTS)+'</main>'+footer()+'<script src="/app.js"></script></body></html>')
print('Rendered',len(PROJECTS),'case pages and 4 disciplines')
