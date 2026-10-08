# REX Portfolio — Developer Handoff

This is the editable source and ready-to-serve output of Cyrus Rex's current portfolio. You can host it independently without ChatGPT, a backend, a database, or access to the original account.

## Snapshot

- Packaged: 8 October 2026 (UTC)
- Existing portfolio: https://rex-visual-world.cyrus-rex.chatgpt.site
- Verified published version: 8
- Source commit: `4ab1cd0918fdb757cf9a71af427ad82e0eb23aff`
- Included: 17 HTML pages, 122 images, 9 MP4 videos, 2 local WOFF2 fonts with their licenses, CSS, JavaScript, JSON content and Python source.
- `dist/` and `render_site.py` are unchanged from that source commit. The README, portable validator and checksum manifest are handoff additions.

The existing hosted site is owner-private. This archive is a standalone copy; it contains no login credentials and grants no hosting, domain, repository, Library or account access. Arrange those separately with Cyrus if needed. No external sharing, deployment or access change was made to prepare this handoff.

## Quick start

Unzip the archive, then open a terminal in the `REX-Portfolio` directory.

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:8000/ in a browser. Stop with Ctrl+C. On Windows, use `py -3` instead of `python3` if that is the available launcher.

Python 3.10+ is recommended. The preview/build/portable-validator steps use only Python's standard library. There is no npm install step. Python's development server is for local preview, not production hosting.

Do not preview by double-clicking `index.html`: the site uses root-relative URLs such as `/style.css`, `/assets/...` and `/work/cambrook/`, which expect an HTTP server rooted at `dist/`.

## File map

| Path | Purpose |
| --- | --- |
| `dist/` | Complete publishable static website; upload this directory's **contents** to your web root. |
| `dist/content.json` | Editable project data, album ordering, media paths, alt text, captions and source provenance IDs. |
| `render_site.py` | Current HTML generator; reads `dist/content.json` and writes the pages in `dist/`. Also contains the homepage/about/footer/contact copy and navigation. |
| `dist/style.css` | All layout, typography, responsive styles and appearance. |
| `dist/app.js` | Video playback, sound handling, image lightboxes and About-section behavior. |
| `dist/assets/` | All media copied into the current source, including some retained assets that are no longer actively referenced. |
| `validate_package.py` | Portable, read-only check of local HTML/CSS/JSON references, anchors and optional JavaScript syntax. No Git history needed. |
| `SHA256SUMS.txt` | SHA-256 digest for every other file in this handoff. |
| `legacy/` | Original historical import, migration and regression scripts, preserved for source completeness. Not the current build workflow. |

Git history, caches, compiled Python files, platform project-binding configuration and credentials are intentionally not included.

## Edit and rebuild

1. Edit project data in `dist/content.json`. Keep IDs and file paths stable unless intentionally changing URLs.
2. Put new media inside `dist/assets/`. Use paths beginning `/assets/` in the JSON. Images use `type: "image"`, `src`, `alt`, and optional dimensions/caption; videos use `type: "video"`, `src`, optional `poster`, `alt` and `loop`.
3. Edit `render_site.py` for homepage text, the About section, contact information, navigation, metadata or HTML templates. Some top-level JSON fields are historical: current contact links, portrait and About video are also hard-coded in the generator, so changing JSON alone will not update those areas.
4. Edit `dist/style.css` and `dist/app.js` directly for styling and interaction changes. The generator does not overwrite these files or any media.
5. Rebuild and validate:

```sh
python3 render_site.py
python3 validate_package.py
```

Rebuilding overwrites generated HTML. Make lasting HTML changes in the generator, rather than only in an output page. The supplied directory tree is part of the build input: retain the discipline directories and `dist/project/`. The generator creates new project/album directories but does not clean obsolete output directories when content is removed; review obsolete routes deliberately.

`legacy/assemble_content.py` and `legacy/update_v4.py` were one-time import/migration scripts. They refer to their original media-staging folders, which are not required for this current snapshot and are not included. Do not run them as a build step: they can recreate older content. `legacy/validate_site.py` checks historical Git revisions and requires that original history plus `ffprobe`; it cannot run from this history-free archive. Use the portable validator instead.

## Deploy anywhere with static hosting

Configure the publish/output directory as `dist`. No server runtime, environment variables, API keys, database or build dependencies are required. If your host requires a build command and provides Python, use `python3 render_site.py`; otherwise deploy the already-built `dist/` output with no build command.

- Serve `dist/index.html` at the domain root `/`.
- Enable ordinary directory indexes so `/photography/` serves `photography/index.html`, and `/work/cambrook/` serves `work/cambrook/index.html`.
- Keep all nested folders and assets intact. Do not flatten them or publish only `index.html`.
- This is a multipage site. An SPA fallback redirect to the homepage is not required.
- Use a domain root or subdomain, for example `https://portfolio.example.com/`. Hosting at a path such as `https://example.com/portfolio/` requires updating root-relative URLs in the generator, JSON, CSS and output, or configuring an appropriate reverse proxy. The archive does not implement a configurable base path.
- Serve HTML, CSS, JavaScript, WebP/JPEG, WOFF2 and MP4 with appropriate MIME types. HTTPS and byte-range support are recommended for production media delivery.
- Check the host's individual-file and total-upload limits for the bundled videos.
- If deploying publicly, agree on that audience and domain with Cyrus first; the original site is currently private.

There is no contact-form backend: contact links open email, Instagram and WhatsApp. The original platform's private-access gate is not part of this static source. A new static host is public unless you configure access controls there.

## Fonts, credits and media rights

Archivo and Instrument Serif are bundled with their original SIL Open Font License files under `dist/assets/fonts/`. Keep those notices with the fonts. `dist/style.css` additionally loads DM Sans and Manrope from Google Fonts via an external `@import`; those two fonts require network access and otherwise use the declared fallbacks. For fully self-hosted fonts, the developer should obtain their font files and license notices and update the CSS.

The existing photography captions and lightbox credits are preserved:

- `assets/photography/01.webp`: Photo editing by Cyrus Rex; original photograph by Katherine Chase / Unsplash.
- `assets/photography/02.webp`: Photo editing by Cyrus Rex; original photograph by Matthew McBrayer / Unsplash.
- `assets/photography/03.webp`: Photo editing by Cyrus Rex; original photograph by Vino Li / Unsplash.
- `assets/photography/04.webp`: Photo editing by Cyrus Rex; original photograph by Zach Inglis / Unsplash.

Other media is provided as the portfolio's existing web-ready assets. This handoff does not grant a new media license or independently verify underlying rights. Preserve credits and confirm any new distribution/use with Cyrus. Original high-resolution or editable design/video project files (PSD, AI, Premiere, etc.) are not part of this website source archive.

## Current pages and behavior

The six main case studies are Cambrook, LOIS CHLOÉ, DESIGNORA, Travel Agencies, AFTERTASTE and SOLE FREQUENCY. There are four discipline pages, a generic work index and five legacy album redirect pages. The SFX/VFX discipline currently displays the existing "Selected work coming soon" placeholder.

The source includes responsive CSS, album-scoped image lightboxes, keyboard controls, muted video behavior, reduced-motion handling and a deferred About background video. These describe implemented behavior, not a claim that every browser interaction has been tested.

## Verification and remaining QA

Packaging checks on 8 October 2026:

- Source commit agrees with the latest saved version and its successful production deployment.
- `dist/` and `render_site.py` match the committed source byte for byte.
- Rebuilding the extracted snapshot reproduces all 17 supplied HTML pages exactly.
- All local HTML/CSS/JSON file references and page anchors resolve.
- JSON and Python parse; JavaScript syntax passes Node's syntax check.
- All 122 images and all 9 videos decode successfully with the available image/video tools.
- ZIP integrity and its extracted SHA-256 manifest pass.

Remaining developer QA: visual review on desktop/mobile, real browser video playback and autoplay restrictions, lightbox open/close/Escape/swipe/focus behavior, back/forward navigation, accessibility and reduced-motion checks, and behavior after deployment to the chosen host. Interactive browser QA and the owner's private production page were not independently revalidated for this handoff. External destinations and Google Fonts availability are not checked by the portable validator.

To verify the packaged checksums on a platform with GNU coreutils, run `sha256sum -c SHA256SUMS.txt` from this directory. The expected checksums describe this original handoff; intentional edits will naturally change them.
