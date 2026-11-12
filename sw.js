// Service worker: network-first for pages (always fresh), cache-first for static assets.
// Bump VERSION whenever you change CSS/JS so visitors get the new files.
const VERSION = "v2";
const CACHE = `dn-${VERSION}`;
const BASE = new URL(self.registration.scope).pathname; // "/" on your domain, "/davidnewman-site/" on GitHub Pages
const PRECACHE = ["", "work/", "about/", "contact/", "offline.html", "assets/css/styles.css", "assets/js/main.js"].map((p) => BASE + p);

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);
  if (request.method !== "GET" || url.origin !== location.origin) return;
  // Never cache the NDA case study
  if (url.pathname.startsWith(BASE + "work/rio-tinto")) return;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((res) => { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(request, copy)); return res; })
        .catch(() => caches.match(request).then((r) => r || caches.match(BASE + "offline.html")))
    );
    return;
  }

  if (url.pathname.startsWith(BASE + "assets/")) {
    event.respondWith(
      caches.match(request).then((cached) => cached || fetch(request).then((res) => {
        if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(request, copy)); }
        return res;
      }))
    );
  }
});
