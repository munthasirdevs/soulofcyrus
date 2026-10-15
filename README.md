# REX Studio Portfolio

A buildless, standalone static portfolio for Cyrus Rex (Creative/Art Director & Designer).

## Project Structure

- `index.html` — Homepage (hero video, interactive practice section, selected work index, about section, contact footer)
- `work/` — Project case studies and galleries:
  - `work/aftr/` — AFTR fragrance branding case with concave ribbon gallery
  - `work/cambrook/` — Cambrook campaign presentation
  - `work/designora/` — DESIGNORA interior studio visual series
  - `work/food-beverage/` — AFTERTASTE food and beverage films and stills
  - `work/lois-chloe/` — LOIS CHLOÉ beauty imagery and film albums
  - `work/sole-frequency/` — SOLE FREQUENCY sneaker visual collection
  - `work/travel-agencies/` — Destination travel campaign designs
- `design/`, `film/`, `photography/`, `sfx-vfx/` — Dedicated discipline showcase pages
- `project/index.html` — Complete work index landing
- `style.css` — Core portfolio styles, typography, and responsive layouts
- `gallery.css` — Floating navigation, work index, concave gallery, project dock, and full-view lightbox
- `cursor.css` + `cursor.js` — Custom desktop cursor with inverted contrast and drag feedback
- `app.js` — Core interactions, concave gallery geometry, dialog full-view modal, video playback controls
- `aftr-curved.css` + `aftr-route.js` — AFTR brand presentation and routing
- `content.json` — Structured portfolio dataset (projects, albums, media, and credits)
- `assets/` — Images, campaign reels, motion posters, brand marks, and variable web fonts

## Preview Locally

Start a local HTTP server directly from the repository root:

```bash
# Using Python 3:
python3 -m http.server 8000

# Or on Windows:
py -3 -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

## Deployment

This website is buildless and ready for direct static deployment:
- **GitHub Pages**: Configure GitHub Pages to serve from the repository root (`/`) on the `main` branch.
- **Netlify / Vercel / Cloudflare Pages**: Deploy the repository root directly without any build command.
