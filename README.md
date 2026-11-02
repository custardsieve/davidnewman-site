# davidnewman.com.au

Portfolio site for David Newman — plain HTML, CSS and JavaScript. No build step, no framework, no database, no server code.

## Structure

```
/                      Home
/work/                 Case study index
/work/<project>/       Case studies (rio-tinto is NDA, protected by Cloudflare Access)
/about/                About + résumé
/contact/              Contact (form via Formspree)
/404.html  /offline.html
/assets/css/styles.css Design tokens + all styles
/assets/js/main.js     Progressive enhancements only (reveal, TOC, service worker)
/assets/img/<project>/ Images
/assets/fonts/         CircularStd (licensed — keep this repo private)
manifest.webmanifest   App (PWA) manifest
sw.js                  Service worker (offline support)
_headers               Security headers (CSP, HSTS…) for Cloudflare Pages
_redirects             Old WordPress URLs → new pages
scripts/               One-off helpers (not served)
```

## First-time setup

1. **Pull images and fonts from the old WordPress site** (while it's still online):
   ```
   node scripts/pull-assets.mjs
   ```
2. **Add your CV** as `assets/david-newman-cv.pdf`.
3. **Contact form:** create a free form at formspree.io and replace `FORM_ID` in `contact/index.html`.
4. **LinkedIn:** add your URL in `contact/index.html` (search for `TODO`).

## Run locally

```
npx serve .
```
Then open http://localhost:3000.

## Deploy (Cloudflare Pages)

1. Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git → pick this repo.
2. Framework preset: **None**. Build command: *(empty)*. Output directory: `/`.
3. Add custom domain `davidnewman.com.au` (Cloudflare will guide the DNS change from VentraIP).

## Protect the NDA case study (Cloudflare Access)

Zero Trust → Access → Applications → Add → Self-hosted → path `davidnewman.com.au/work/rio-tinto/*` → policy: allow specific emails (or one-time PIN to any email you approve).
The NDA content itself is **not** in this repo — add it to `work/rio-tinto/index.html` only once Access is switched on.

## Updating

- Edit the HTML, commit, push — Cloudflare redeploys in about a minute.
- After changing CSS or JS, bump `VERSION` in `sw.js` so returning visitors get the new files.
- New case study: copy `work/officeworks/` to `work/<new-slug>/`, edit, and add a card to `/` and `/work/`, plus a line in `sitemap.xml`.
