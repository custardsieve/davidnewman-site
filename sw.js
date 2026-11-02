// Service worker: network-first for pages (always fresh), cache-first for static assets.
// Bump VERSION whenever you change CSS/JS so visitors get the new files.
const VERSION = "v1";
const CACHE = `dn-${VERSION}`;
const PRECACHE = ["/", "/work/", "/about/", "/contact/", "/offline.html", "/assets/css/styles.css", "/assets/js/main.js"];

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
  if (url.pathname.startsWith("/work/rio-tinto")) return;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((res) => { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(request, copy)); return res; })
        .catch(() => caches.match(request).then((r) => r || caches.match("/offline.html")))
    );
    return;
  }

  if (url.pathname.startsWith("/assets/")) {
    event.respondWith(
      caches.match(request).then((cached) => cached || fetch(request).then((res) => {
        if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(request, copy)); }
        return res;
      }))
    );
  }
});
