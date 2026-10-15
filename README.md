# soulofcyrus Portfolio

> **Creative/Art Director & Designer**  
> Design · Film · Photography · SFX & VFX  
> *Based in Dhaka & Athens*

[![Static Architecture](https://img.shields.io/badge/Architecture-Buildless%20Static-101010?style=for-the-badge)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![Design](https://img.shields.io/badge/Discipline-Design%20%2F%20Film%20%2F%20Photo%20%2F%20VFX-gray?style=for-the-badge)](https://instagram.com/soulofcyrus)

---

## Overview

A high-performance, buildless creative portfolio showcasing the multidisciplinary works of **Cyrus Rex**. Built with pure vanilla technologies—delivering cinematic aesthetics, smooth micro-interactions, responsive typography, and WebGL-powered 3D experiences without bundlers or heavy framework overhead.

---

## Core Features & Experience

- **Zero-Build Static Architecture**: Clean HTML5, modern vanilla CSS, and modular ES JavaScript. Deploys instantly to any static host with zero build step.
- **Concave 3D Ribbon Showcase (AFTR)**: Interactive Three.js / WebGL cylindrical canvas gallery featuring smooth inertia drag and full-view media expansion.
- **Kinetic Custom Cursor**: Dynamic inverted-contrast cursor with trailing physics, magnetic element snapping, and context-aware drag badges.
- **Smart Video Player System**: Synchronized playback engine with `IntersectionObserver` auto-pause/resume, independent audio unmuting, and accessibility toggles.
- **Accessible & Motion-Conscious**: Native dialog full-view lightbox, semantic ARIA landmarks, keyboard focus management, and automatic adaptation for `prefers-reduced-motion`.
- **Responsive Typography & Grids**: Fluid typography powered by `clamp()` using variable *Archivo* and *Instrument Serif* italic fonts, adapting seamlessly from mobile screens to ultrawide displays.

---

## Project Structure

```
├── index.html                    # Root landing page (hero reel, selected works, about, contact)
├── style.css                     # Global design system, typography tokens, layout grids
├── gallery.css                   # Case study layouts, media grids, lightbox dialog styles
├── cursor.css / cursor.js        # Custom desktop trailing cursor system
├── app.js                        # App controller, media observers, video sync, menu toggles
├── aftr.css / aftr.js            # AFTR 3D WebGL ribbon canvas and interactive shaders
├── aftr-curved.css / aftr-route.js # Curved viewport layout rules and experience routing
├── content.json                  # Structured portfolio data (projects, media, credits)
│
├── project/
│   └── index.html                # Global work directory and index archive
│
├── design/                       # Discipline Hub: Visual identities & editorial design
│   └── index.html
├── film/                         # Discipline Hub: Direction, cinematography & motion reels
│   └── index.html
├── photography/                  # Discipline Hub: Editorial, studio & portrait photography
│   └── index.html
├── sfx-vfx/                      # Discipline Hub: Visual effects, 3D simulations & composites
│   └── index.html
│
├── work/                         # Project Case Studies & Dedicated Galleries
│   ├── aftr/                     # AFTR fragrance brand identity & campaign
│   │   ├── index.html
│   │   └── curved/index.html     # Dedicated cylindrical ribbon experience
│   ├── cambrook/                 # Cambrook social media campaign & motion
│   │   └── index.html
│   ├── designora/                # DESIGNORA interior studio visual series
│   │   └── index.html
│   ├── designora-01/             # DESIGNORA Volume 01 collection
│   │   └── index.html
│   ├── designora-02/             # DESIGNORA Volume 02 collection
│   │   └── index.html
│   ├── food-beverage/            # AFTERTASTE culinary cinematography & stills
│   │   └── index.html
│   ├── lois-chloe/               # LOIS CHLOÉ beauty imagery & multi-album films
│   │   └── index.html
│   ├── lois-lip-oil/             # LOIS CHLOÉ Lip Oil product showcase
│   │   └── index.html
│   ├── lois-lipstick/            # LOIS CHLOÉ Lipstick product showcase
│   │   └── index.html
│   ├── lois-sunscreen/           # LOIS CHLOÉ Sunscreen product showcase
│   │   └── index.html
│   ├── sole-frequency/           # SOLE FREQUENCY sneaker visual collection
│   │   └── index.html
│   └── travel-agencies/          # Destination travel campaign designs
│       └── index.html
│
└── assets/                       # Static production assets
    ├── brand/                    # Brand marks and vector wordmarks
    ├── fonts/                    # Self-hosted variable web fonts (WOFF2)
    ├── hero/                     # Hero cinematography video and poster assets
    ├── projects/                 # High-resolution project imagery, videos, and film posters
    └── thumbnails/               # Optimized WebP thumbnails for project grids
```

---

## Local Development & Preview

Because this is a completely static, buildless project, you can run it locally with any simple HTTP file server:

### Using Python
```bash
# Python 3 (macOS / Linux):
python3 -m http.server 8000

# Python on Windows:
py -3 -m http.server 8000
```

### Using Node.js
```bash
# Using npx and serve:
npx serve .

# Or using http-server:
npx http-server -p 8000
```

### Using VS Code / IDE
Install the **Live Server** extension, right-click `index.html`, and select **Open with Live Server**.

Open `http://localhost:8000` in your web browser.

---

## Deployment

The repository is configured for immediate deployment across all modern static hosting providers:

| Provider | Configuration | Build Command | Publish Directory |
| :--- | :--- | :--- | :--- |
| **GitHub Pages** | Settings → Pages → Deploy from branch `main` / `(root)` | *None* | `/` (root) |
| **Netlify** | Connect GitHub repo | *Leave empty* | `.` (root) |
| **Vercel** | Import Git repository → Framework: *Other* | *Leave empty* | `.` (root) |
| **Cloudflare Pages** | Connect Git repository | *Leave empty* | `.` (root) |

---

## Contact & Inquiries

- **Email**: [rex.studio.bd@gmail.com](mailto:rex.studio.bd@gmail.com)
- **Instagram**: [@soulofcyrus](https://www.instagram.com/soulofcyrus/)
- **WhatsApp**: [+880 1938 466771](https://wa.me/8801938466771)

---

&copy; 2026 CYRUS REX. All rights reserved.
