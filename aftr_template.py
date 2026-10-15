"""Straight, full-height presentation for the AFTR brand case only."""
from html import escape as E

def aftr_page(p,head,header):
 out=head(p['title']).replace('</head>','<link rel="stylesheet" href="/aftr.css"></head>')+'<body class="aftr-page" id="top">'+header()
 out+='<main id="main" class="aftr-rail" tabindex="0" aria-label="AFTR case study. Scroll sideways or use arrow keys. Select artwork for full view."><h1 class="sr-only">AFTR — A self-initiated fragrance identity by Cyrus Rex</h1>'
 for i,a in enumerate(p['media']):
  out+=f'<section class="aftr-panel" id="{E(a["id"])}" data-chapter="{E(a["chapter"])}" style="--media-ratio:{a["width"] / a["height"]:.5f}" aria-label="{E(a["chapter"])}"><button class="case-open" type="button" data-type="{a["type"]}" data-full="{E(a["src"])}" data-caption="{E(a["alt"])}" aria-label="Open {E(a["alt"])} in full view">'
  if a['type']=='video':
   out+=f'<video autoplay muted loop playsinline preload="metadata" poster="{E(a.get("poster",""))}" aria-label="{E(a["alt"])}"><source src="{E(a["src"])}" type="video/mp4"></video>'
  else:
   out+=f'<img src="{E(a["src"])}" alt="{E(a["alt"])}" width="{a["width"]}" height="{a["height"]}" '+('fetchpriority="high"' if i==0 else 'loading="lazy"')+'>'
  out+='</button></section>'
 out+='</main><div class="aftr-caption"><a href="/#work">SELECTED WORK</a><span class="case-current">01 / '+f'{len(p["media"]):02}'+'</span><span class="case-chapter"></span></div>'
 out+='<div class="aftr-tools"><span>SCROLL TO EXPLORE</span><div><button class="case-motion" type="button" aria-pressed="false">Pause film</button><button class="case-prev" type="button" aria-label="Previous panel">←</button><button class="case-next" type="button" aria-label="Next panel">→</button></div></div>'
 out+='<aside class="project-dock" aria-label="Project information"><div class="dock-header"><span class="dock-title">AFTR</span><button class="dock-about" type="button" aria-expanded="false" aria-controls="project-details">[ ABOUT ]</button></div><div class="dock-body"><div class="dock-details" id="project-details" hidden><h2 class="dock-headline">What remains.</h2><dl><div><dt>01 / PROJECT</dt><dd>AFTR<br>Self-initiated fragrance concept</dd></div><div><dt>02 / DISCIPLINE</dt><dd>Brand identity, product concept and campaign art direction</dd></div><div><dt>03 / DESIGNER</dt><dd>Cyrus Rex</dd></div><div><dt>04 / APPROACH</dt><dd>A study in contrast: precise glass, tactile stone and an oxide-red wordmark. An identity explored through form, packaging and image.</dd></div></dl></div><p class="dock-summary">A fragrance identity shaped around what remains.</p><div class="dock-bottom"><label class="progress-control"><span class="case-progress">0%</span><input class="case-range" type="range" min="0" max="100" step="0.1" value="0" aria-label="AFTR presentation progress"></label><a class="explore-more" href="/#work">[ EXPLORE MORE ]</a></div></div></aside><p class="sr-only case-announcement" aria-live="polite"></p><script src="/app.js"></script><script src="/aftr.js"></script></body></html>'
 return out
