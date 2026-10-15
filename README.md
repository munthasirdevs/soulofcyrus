# REX Studio portfolio

A buildless static portfolio. Serve the `dist` folder as the web root.

## Edit and build

- `dist/content.json` is the approved project, album, media and credit record.
- `render_site.py` generates the HTML routes from that record.
- `dist/style.css` contains the original homepage, hero and About styling.
- `dist/gallery.css` contains the current floating navigation, white work index, gallery, project dock and full-view styling.
- `dist/app.js` owns playback, menus, concave gallery geometry, album/history navigation and the full-view dialog.
- `dist/cursor.css` and `dist/cursor.js` provide the desktop rounded-square cursor, inverted contrast, link/click feedback and gallery View/Drag states. Native pointers remain for modal viewers, form/video controls, keyboard navigation, reduced motion and touch input.
- `dist/assets` includes all local images, videos, logo and fonts. Font licenses live in `dist/assets/fonts`.

After HTML/template changes run:

```bash
python3 render_site.py
# Or on Windows:
py -3 render_site.py
```

To preview locally, serve the `dist` folder as the web root:

```bash
python3 -m http.server 8000 --directory dist
# Or on Windows:
py -3 -m http.server 8000 --directory dist
```

Then open `http://localhost:8000` in your browser. Absolute asset and route paths require the web root to be configured to `dist`.

## Gallery behavior

Desktop opens on the first seven cards in a concave ribbon: the centre is smaller and farther away, while the outer cards grow and turn inward. Small screens show a reduced, touch-draggable window. Wheel gestures, drag/swipe, arrow buttons, arrow keys, Home/End and the progress control move the gallery. Progress runs from the opening group to the final artwork. Album links keep their own URL fragments; old album URLs redirect to the matching current album.

Selecting a card opens a full-viewport, uncropped image or film. Close or Escape returns to the gallery. Previous/next controls stay within that album. The selected lipstick cover keeps its approved 90-degree rotation in both views. Original photography credits remain in the image captions.

Films appear before stills and start muted. Pause films persists across scrolling, album switching and returning from full view. Reduced motion starts all decorative video paused. The About background still uses the supplied landscape Bold Boho film.

## Verification

The dependency-free validator checks the approved content hash, route references, album/media sequence, credits, rotation, navigation hooks and JavaScript syntax. In a checkout with Site history it also compares all 135 original asset bytes against the previous version. If intentionally changing content later, update its expected baseline after review.

This revision received source regression checks and simulated-DOM interaction tests. Actual browser visual/playback QA was unavailable in the build environment because browser startup and local-preview routing were blocked. Validate final appearance and real touch/video playback in the target browsers before an external public launch.

## AFTR brand case

AFTR uses the shared concave gallery at `/work/aftr/`, with the same filled,
rounded preview cards as photography. Full view contains the complete artwork.
AFTR-specific typography and black controls remain in `dist/aftr-curved.css`. It is the only
visible AFTR presentation. The former `/work/aftr/curved/` route redirects to
the canonical route, preserving query strings and fragments. `aftr-route.js`
resolves the saved straight layout's artwork fragments, including `/view`.

All 15 supplied assets retain their approved order: 14 stills, then film.
AFTR remains first in the work index with the approved male-cheek thumbnail.
The original six projects and their media are unchanged. The work is a
self-initiated fragrance concept by Cyrus Rex.

## Saved branding preset

`layouts.json` retains the reusable **Straight full-height branding** preset,
implemented by `aftr_template.py`, `dist/aftr.css`, and `dist/aftr.js`. It is kept
in source for future branding projects, without a second published AFTR page.
The preset retains approved margins, contained imagery, continuous wheel
behavior, and supplied media order. Prior straight AFTR revisions also remain
in source history.

Project index rows retain a 32px desktop / 28px mobile vertical gap; image
column widths and thumbnail sizing are unchanged.

Additional checks: `node test_cursor.js`, `node test_aftr.js`, `node test_curved.js`, and
`node test_aftr_routes.js` cover simulated interactions and redirect/deep-link
behavior. These do not establish real browser rendering, wheel input, video
decoding, or touch behavior. Native browser QA remains unverified.
