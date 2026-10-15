from pathlib import Path
from html import escape as E
import json
from aftr_template import aftr_page
ROOT=Path(__file__).parent/'dist'
DATA=json.loads((ROOT/'content.json').read_text(encoding='utf-8'))
PROJECTS=DATA.get('projects',[])
LAYOUTS=json.loads((Path(__file__).parent/'layouts.json').read_text(encoding='utf-8'))
ICON="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23101010'/%3E%3Ctext x='10' y='49' fill='white' font-size='48' font-family='Arial' font-weight='bold'%3ER%3C/text%3E%3C/svg%3E"
def head(title):return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101010"><meta name="description" content="Cyrus Rex. Creative/Art Director. Designer. Design, Film, Photography and SFX/VFX. Based in Dhaka and Athens."><title>{E(title)} — CYRUS REX</title><link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/gallery.css"><link rel="stylesheet" href="/cursor.css"><script src="/cursor.js" defer></script><link rel="icon" href="{ICON}"><link rel="preload" href="/assets/fonts/instrument-serif-italic.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/archivo-variable.woff2" as="font" type="font/woff2" crossorigin></head>'''
def header():return '''<a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="wordmark" href="/" aria-label="Rex Studio home"><img src="/assets/brand/rex-studio-white.png" width="1279" height="264" alt="REX Studio"></a><div class="nav-actions"><a class="contact-pill" href="mailto:rex.studio.bd@gmail.com">[ CONTACT ]</a><button class="menu-toggle" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="site-menu"><span aria-hidden="true">+</span></button></div><nav class="site-menu" id="site-menu" aria-label="Main navigation" hidden><div class="menu-links"><a href="/#work">[ WORK ]</a><a href="/#about">[ ABOUT ]</a><a href="/#contact">[ CONTACT ]</a></div><div class="menu-disciplines"><a href="/design/">Design</a><a href="/film/">Film</a><a href="/photography/">Photography</a><a href="/sfx-vfx/">SFX/VFX</a></div><div class="menu-bottom"><span>DHAKA / ATHENS</span><a href="https://www.instagram.com/soulofcyrus/" target="_blank" rel="noopener noreferrer">INSTAGRAM ↗</a></div></nav></header>'''

def footer():return '''<footer id="contact" class="pad"><div class="folio"><span>LET’S MAKE SOMETHING</span><span>CYRUS REX</span></div><a class="contact-title pairing" href="mailto:rex.studio.bd@gmail.com"><span>I got the ingredients,</span><strong>LET’S COOK.</strong></a><div class="social-links social-icons" role="group" aria-label="Contact Rex"><a href="mailto:rex.studio.bd@gmail.com" aria-label="Email Rex" title="Email"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/></svg></a><a href="https://www.instagram.com/soulofcyrus/" target="_blank" rel="noopener noreferrer" aria-label="Rex on Instagram" title="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true" focusable="false"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a><a href="https://wa.me/8801938466771" target="_blank" rel="noopener noreferrer" aria-label="Chat with Rex on WhatsApp" title="WhatsApp"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20.5 11.7a8.5 8.5 0 0 1-12.7 7.4L3 20.5l1.4-4.7a8.5 8.5 0 1 1 16.1-4.1Z"/><path d="M8.2 7.3c-.4 0-1.2.8-1.2 1.8 0 2.7 4 6.7 6.9 6.7 1 0 1.8-.8 1.8-1.2l-2.2-1.5-.9 1c-1.4-.5-2.4-1.5-2.9-2.9l1-.9-1.4-3Z"/></svg></a></div><div class="footer-base"><span>© 2026 CYRUS REX</span><span>DESIGN / FILM / PHOTOGRAPHY / SFX & VFX</span><a href="#top">Back to top</a></div></footer>'''
def folio(n):return f'<div class="folio case-folio"><span>{n}</span><span>CREATIVE/ART DIRECTOR. DESIGNER</span><a href="mailto:rex.studio.bd@gmail.com">rex.studio.bd@gmail.com</a><span>© 2026</span></div>'
def picture(a,cls='',lazy=True):return f'<img class="{cls}" src="{E(a["src"])}" alt="{E(a.get("alt","Project visual"))}"'+(' loading="lazy"' if lazy else ' fetchpriority="high"')+(f' width="{a["width"]}" height="{a["height"]}"' if a.get('width') else '')+'>'
def thumbnail(a):
 if a['type']=='video':return f'<video class="thumbnail-video" autoplay muted loop playsinline preload="metadata" poster="{E(a.get("poster",""))}" aria-label="{E(a.get("alt","Project film"))}"><source src="{E(a["src"])}" type="video/mp4"></video><span class="thumbnail-badge">FILM</span>'
 return picture(a)
def rows(projects):
 out=''
 for p in projects:
  idx=PROJECTS.index(p)+1
  out+=f'''<article class="work-row"><a class="work-visual" href="/work/{p['id']}/" aria-label="Explore {E(p['title'])}" style="--image-bg:{p.get('color','#eeeeee')}">{thumbnail(p.get('thumbnail',p['cover']))}</a><a class="work-copy" href="/work/{p['id']}/" aria-label="Explore {E(p['title'])}"><dl class="project-meta"><div><dt>Project</dt><dd><h3>{E(p['title'])}</h3></dd></div><div><dt>Field</dt><dd>{E(p['category'])}</dd></div><div><dt>Format</dt><dd>{E(p['format'])}</dd></div></dl><span class="work-index">{idx:02} / {len(PROJECTS):02} <span aria-hidden="true">↗</span></span></a></article>'''
 return out

def ribbon(g):
 assets=g['media'] if g.get('preserve_media_order') else [a for a in g['media'] if a['type']=='video']+[a for a in g['media'] if a['type']!='video']
 out=f'<section class="ribbon-group" id="{g["id"]}" data-title="{E(g["title"])}" data-intro="{E(g["intro"])}" data-format="{E(g.get("format","Photography / Photo editing"))}" data-focus="{E(g.get("focus","Light / Composition / Image making"))}" aria-label="{E(g["title"])} gallery"><div class="ribbon-stage" tabindex="0" role="region" aria-label="{E(g["title"])}. Scroll or use arrow keys to browse. Select an image for full view."><div class="ribbon-scroll" aria-hidden="true" tabindex="-1"><div class="ribbon-track"></div></div><div class="ribbon-cards">'
 for i,a in enumerate(assets):
  rot=g.get('cover',{}).get('rotation',0) if a['src']==g.get('cover',{}).get('src') else a.get('rotation',0)
  out+=f'<figure class="ribbon-card" data-index="{i}"><button class="gallery-open" type="button" data-type="{a["type"]}" data-full="{E(a["src"])}" data-caption="{E(a.get("caption",a.get("alt","")))}" data-rotation="{rot}" data-width="{a.get("width",0)}" data-height="{a.get("height",0)}" aria-label="Open {E(a.get("alt",g["title"]))} in full view">'
  if a['type']=='video':
   out+=f'<video autoplay muted loop playsinline preload="metadata" poster="{E(a.get("poster",""))}" aria-label="{E(a.get("alt","Project film"))}" tabindex="-1"><source src="{E(a["src"])}" type="video/mp4"></video><span class="card-film">FILM ↗</span>'
  else:out+=picture(a,lazy=False if i<7 else True)
  out+='<span class="card-open" aria-hidden="true">↗</span></button>'
  if a.get('caption'):out+=f'<figcaption class="sr-only">{E(a["caption"])}</figcaption>'
  out+='</figure>'
 return out+'</div></div></section>'

def project_page(p,groups,i=None):
 title=p['title'];out=head(title)+'<body class="case-page ribbon-page" id="top">'+header()+f'<main id="main" class="ribbon-main"><h1 class="sr-only">{E(title)}</h1><div class="gallery-heading"><a href="/#work">[ SELECTED WORK ]</a><span>{E(p.get("category","Photography / Photo editing"))}</span></div>'
 out+=f'<nav class="album-tabs" aria-label="{E(title)} albums">'+''.join(f'<a href="#{g["id"]}" data-album="{g["id"]}"><span>{j:02}</span> {E(g["title"])}</a>' for j,g in enumerate(groups,1))+'</nav>'
 out+=''.join(ribbon(g) if j==0 else ribbon(g).replace('<section class="ribbon-group"','<section hidden class="ribbon-group"',1) for j,g in enumerate(groups))
 out+='<div class="gallery-tools"><p>SCROLL TO EXPLORE <span aria-hidden="true">↔</span></p><div><button class="gallery-motion" type="button" aria-pressed="false" hidden>Pause films</button><button class="gallery-prev" type="button" aria-label="Move gallery left">←</button><button class="gallery-next" type="button" aria-label="Move gallery right">→</button></div></div></main>'
 overview=''
 if p.get('headline') and p['headline']!=title:overview+=f'<h2 class="dock-headline">{E(p["headline"])}</h2>'
 if p.get('albums'):overview+=f'<p class="dock-overview">{E(p["intro"])}</p>'
 out+=f'<aside class="project-dock" aria-label="Project information"><div class="dock-header"><span class="dock-title">{E(title)}</span><button class="dock-about" type="button" aria-expanded="false" aria-controls="project-details">[ ABOUT ]</button></div><div class="dock-body"><div class="dock-details" id="project-details" hidden>{overview}<dl><div><dt>01 [ PROJECT ]</dt><dd class="detail-project">{E(title)}</dd></div><div><dt>02 [ FORMAT ]</dt><dd class="detail-format"></dd></div><div><dt>03 [ FOCUS ]</dt><dd class="detail-focus"></dd></div>'
 if p.get('context'):out+='<div><dt>04 [ CONTEXT ]</dt><dd>'+E(p['context'])+(f' <a href="{E(p["source"])}" target="_blank" rel="noopener noreferrer">Brand background ↗</a>' if p.get('source') else '')+'</dd></div>'
 out+='</dl></div><p class="dock-summary">'+E(groups[0]['intro'])+'</p><div class="dock-bottom"><label class="progress-control"><span class="gallery-progress">0%</span><input class="gallery-range" type="range" min="0" max="100" step="0.1" value="0" aria-label="Gallery progress"></label><a class="explore-more" href="/#work">[ EXPLORE MORE ]</a></div></div></aside><div class="sr-only gallery-announcement" aria-live="polite"></div><script src="/app.js"></script></body></html>'
 return out

homepage=head('Selected Work')+'<body id="top">'+header()+'''<main id="main"><section class="hero" aria-label="Introduction"><video id="hero-video" autoplay muted loop playsinline preload="metadata" poster="/assets/hero-poster.jpg"><source src="/assets/hero.mp4" type="video/mp4"></video><div class="hero-overlay"></div><div class="hero-top"><span>DESIGN / FILM / PHOTOGRAPHY / SFX & VFX</span><span>PORTFOLIO — 2026</span></div><p class="hero-role">Creative/Art Director.<br>Designer</p><h1 class="hero-name pairing"><span>CYRUS</span><strong>REX</strong></h1><div class="hero-controls"><button id="sound" aria-pressed="false" type="button">Sound off</button><button id="play" type="button">Pause</button></div></section><section id="intro" class="intro pad"><div class="folio"><span>0.1 / THE PRACTICE</span><span>CYRUS REX</span></div><div class="intro-grid"><figure class="portrait"><img src="/assets/portrait/cyrus-rex-chess.webp" alt="Monochrome portrait of Cyrus Rex in a white shirt among floating chess pieces" width="1122" height="1402" loading="lazy"><figcaption>CYRUS REX / CREATIVE PRACTICE</figcaption></figure><div class="intro-copy"><h2 class="pairing"><span>A visual game<br>built on</span><strong>INSTINCT.</strong></h2><p>I’m Rex, a creative/art director and designer. My practice moves across <b>Design, Film, Photography and SFX/VFX.</b></p><div class="practice-tags"><span>01 / DESIGN</span><span>02 / FILM</span><span>03 / PHOTOGRAPHY</span><span>04 / SFX/VFX</span></div></div></div></section><section id="work" class="work pad"><div class="folio"><span>0.2 / SELECTED WORK</span><span>AN INDEX OF IDEAS</span></div><div class="work-heading"><h2 class="pairing"><span>Selected</span><strong>WORK.</strong></h2><p>DESIGN / MOVING IMAGE<br>'''+f'{len(PROJECTS):02} PROJECT STORIES'+'''</p></div>'''+rows(PROJECTS)+'''</section><section id="about" class="about pad"><div class="about-motion" aria-hidden="true"><video id="about-video" autoplay muted loop playsinline preload="none" poster="/assets/about/bold-boho-poster.jpg" tabindex="-1"><source data-src="/assets/about/bold-boho-landscape.mp4" type="video/mp4"></video></div><div class="folio"><span>0.3 / BEHIND THE WORK</span><span>FOUR CONNECTED DISCIPLINES</span></div><h2 class="pairing"><span>An eye for detail.<br>A feel for</span><strong>THE UNEXPECTED.</strong></h2><div class="about-bottom"><p>I’m a creative/art director and designer based in Dhaka and Athens. I work across design, film, photography and SFX/VFX, shaping ideas from the first visual thought to the final frame.</p><nav class="disciplines" aria-label="Explore disciplines">'''+''.join(f'<a href="/{slug}/"><small>{i:02}</small>{label}<small>Explore</small></a>' for i,(slug,label) in enumerate([('design','Design'),('film','Film'),('photography','Photography'),('sfx-vfx','SFX/VFX')],1))+'''</nav></div><button class="about-playback" id="about-playback" type="button" aria-controls="about-video" hidden>Pause background</button></section></main>'''+footer()+'<script src="/app.js"></script></body></html>'
(ROOT/'index.html').write_text(homepage, encoding='utf-8')
for i,p in enumerate(PROJECTS):
 path=ROOT/'work'/p['id'];path.mkdir(parents=True,exist_ok=True)
 groups=p.get('albums',[p])
 if p['id']=='aftr':
  curved=project_page(p,groups,i).replace('<body class="case-page ribbon-page"','<body class="case-page ribbon-page aftr-curved"')
  curved=curved.replace('</head>','<link rel="canonical" href="/work/aftr/"><link rel="stylesheet" href="/aftr-curved.css"></head>')
  for media in p['media']:
   curved=curved.replace('data-full="'+E(media['src'])+'"','data-media-id="'+media['id']+'" data-full="'+E(media['src'])+'"')
  curved=curved.replace('</body>','<script src="/aftr-route.js"></script></body>')
  (path/'index.html').write_text(curved, encoding='utf-8')
  target=path/'curved';target.mkdir(exist_ok=True)
  redirect=head('AFTR').replace('</head>','<link rel="canonical" href="/work/aftr/"><script>location.replace("/work/aftr/"+location.search+location.hash);</script><noscript><meta http-equiv="refresh" content="0; url=/work/aftr/"></noscript></head>')
  (target/'index.html').write_text(redirect+'<body id="top">'+header()+'<main id="main" class="pad"><h1>AFTR</h1><a href="/work/aftr/">Open AFTR</a></main></body></html>', encoding='utf-8')
 else:
  (path/'index.html').write_text((aftr_page(p,head,header) if p.get('presentation')==LAYOUTS['branding']['presentation'] else project_page(p,groups,i)), encoding='utf-8')
 for a in p.get('albums',[]):
  legacy=ROOT/'work'/a['legacy_id'];legacy.mkdir(parents=True,exist_ok=True)
  target=f'/work/{p["id"]}/#{a["id"]}'
  redirect=head(f'{p["title"]} / {a["title"]}').replace('</head>',f'<meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="/work/{p["id"]}/"></head>')
  (legacy/'index.html').write_text(redirect+'<body id="top">'+header()+f'<main id="main" class="pad"><h1 class="index-title">{E(a["title"])}</h1><p>This album is now part of {E(p["title"])}.</p><a class="case-link" href="{target}">Open the {E(a["title"])} album</a></main>'+footer()+'<script src="/app.js"></script></body></html>', encoding='utf-8')
for n,(slug,title,tag,desc) in enumerate([('design','Design','Ideas, made visible.','Visual identities, campaign imagery and editorial design.'),('film','Film','Stories in motion.','Product films, moving-image studies and campaign visuals.'),('photography','Photography','Light. Form. Feeling.','Photography, personal studies and photo editing.'),('sfx-vfx','SFX/VFX','Beyond the frame.','A dedicated space for sound and visual effects.')],1):
 selected=[p for p in PROJECTS if slug in p['disciplines']]
 main=f'<main id="main"><section class="discipline-hero pad"><div class="folio"><span>DISCIPLINE / {n:02}</span><a href="/#about">All disciplines</a></div><h1>{title}</h1><div class="discipline-desc"><h2>{tag}</h2><p>{desc}</p></div></section><section class="discipline-work pad">'+rows(selected)
 if slug=='photography':
  (ROOT/slug/'index.html').write_text(project_page({'title':'Photography','category':'Photography / Photo editing'},DATA['photography_albums']), encoding='utf-8')
  continue
 if not selected and slug!='photography':main+='<div class="empty-selection"><p>Selected work coming soon.</p><a href="/#work">Explore the current work index</a></div>'
 main+='</section><nav class="discipline-nav pad" aria-label="Other disciplines">'+''.join(f'<a href="/{s}/"'+(' aria-current="page"' if s==slug else '')+f'>{t}</a>' for s,t in [('design','Design'),('film','Film'),('photography','Photography'),('sfx-vfx','SFX/VFX')])+'</nav></main>'
 (ROOT/slug/'index.html').write_text(head(title)+f'<body id="top" class="discipline-page">'+header()+main+footer()+'<script src="/app.js"></script></body></html>', encoding='utf-8')
# Preserve the previously published generic case URL as a usable work-index landing.
(ROOT/'project'/'index.html').write_text(head('Work Index')+'<body id="top">'+header()+'<main id="main" class="pad"><h1 class="index-title">Selected work</h1>'+rows(PROJECTS)+'</main>'+footer()+'<script src="/app.js"></script></body></html>', encoding='utf-8')
print('Rendered',len(PROJECTS),'case pages and 4 disciplines')
