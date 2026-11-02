// David Newman Design — progressive enhancements only.
// Everything on the site works without this file.
(() => {
  document.documentElement.classList.remove("no-js");

  // Header border once the page scrolls
  const header = document.querySelector(".site-header");
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // Reveal-on-scroll (skipped when the user prefers reduced motion)
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const revealEls = document.querySelectorAll(".reveal");
  if (!reduceMotion && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      }
    }, { rootMargin: "0px 0px -10% 0px" });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  // Case-study table of contents: highlight the section in view
  const tocLinks = document.querySelectorAll(".cs-toc a[href^='#']");
  if (tocLinks.length && "IntersectionObserver" in window) {
    const byId = new Map([...tocLinks].map((a) => [a.getAttribute("href").slice(1), a]));
    const spy = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          tocLinks.forEach((a) => a.classList.remove("is-active"));
          byId.get(entry.target.id)?.classList.add("is-active");
        }
      }
    }, { rootMargin: "-40% 0px -55% 0px" });
    byId.forEach((_, id) => {
      const section = document.getElementById(id);
      if (section) spy.observe(section);
    });
  }

  // Footer year
  document.querySelectorAll("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });

  // Service worker (offline + installable app)
  if ("serviceWorker" in navigator && location.protocol === "https:") {
    window.addEventListener("load", () => navigator.serviceWorker.register("/sw.js").catch(() => {}));
  }
})();
