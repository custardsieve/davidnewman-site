// David Newman Design — progressive enhancements only.
// Everything on the site works without this file.
(() => {
  const siteRoot = new URL("../../", document.currentScript ? document.currentScript.src : location.href);
  document.documentElement.classList.remove("no-js");

  const header = document.querySelector(".site-header");
  const nav = document.querySelector(".nav");

  if (header) {
    const actions = document.createElement("div");
    actions.className = "site-header__actions";

    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "theme-toggle";
    toggle.setAttribute("aria-label", "Switch to dark mode");
    toggle.setAttribute("aria-pressed", "false");
    const svgNamespace = "http://www.w3.org/2000/svg";
    const themeIcon = document.createElementNS(svgNamespace, "svg");
    themeIcon.className = "theme-toggle__icon";
    themeIcon.setAttribute("viewBox", "0 -960 960 960");
    themeIcon.setAttribute("aria-hidden", "true");
    toggle.appendChild(themeIcon);
    let iconRequest = 0;

    const updateThemeIcon = (isDark) => {
      const request = ++iconRequest;
      const iconName = isDark ? "light_mode_20px.svg" : "dark_mode_20px.svg";
      fetch(new URL(`assets/icons/${iconName}`, siteRoot))
        .then((response) => {
          if (!response.ok) throw new Error("Theme icon could not be loaded");
          return response.text();
        })
        .then((svgText) => {
          const iconDocument = new DOMParser().parseFromString(svgText, "image/svg+xml");
          const sourcePath = iconDocument.querySelector("svg > path");
          const pathData = sourcePath?.getAttribute("d");
          if (request !== iconRequest || !pathData) return;

          const path = document.createElementNS(svgNamespace, "path");
          path.setAttribute("d", pathData);
          path.setAttribute("fill", "currentColor");
          themeIcon.replaceChildren(path);
        })
        .catch(() => {});
    };

    const applyTheme = (theme) => {
      const isDark = theme === "dark";
      document.documentElement.setAttribute("data-theme", theme);
      toggle.setAttribute("aria-pressed", String(isDark));
      toggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
      toggle.title = isDark ? "Switch to light mode" : "Switch to dark mode";
      updateThemeIcon(isDark);
      const themeColor = document.querySelector('meta[name="theme-color"]');
      if (themeColor) themeColor.setAttribute("content", isDark ? "#0c0c0c" : "#ffffff");
      try {
        localStorage.setItem("theme", theme);
      } catch (error) {
        // ignore storage failures in restricted contexts
      }
    };

    const savedTheme = (() => {
      try {
        return localStorage.getItem("theme");
      } catch (error) {
        return null;
      }
    })();

    const preferredTheme = savedTheme || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    applyTheme(preferredTheme);

    toggle.addEventListener("click", () => {
      const nextTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(nextTheme);
    });

    if (nav) {
      nav.after(actions);
    } else {
      header.querySelector(".site-header__inner")?.appendChild(actions);
    }
    actions.appendChild(toggle);

    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Parallax presets: change one value here to adjust the site-wide effect.
  // Options: 'subtle', 'medium', 'strong'
  const PARALLAX_PRESETS = {
    subtle: { strength: 28, scale: 1.08, mobileOff: true },
    medium: { strength: 48, scale: 1.10, mobileOff: true },
    strong: { strength: 80, scale: 1.15, mobileOff: true },
    off: { strength: 0, scale: 1, mobileOff: true }
  };
  const PARALLAX_MODE = "strong";
  const parallaxConfig = PARALLAX_PRESETS[PARALLAX_MODE] || PARALLAX_PRESETS.subtle;

  const parallaxEls = document.querySelectorAll(".parallax");
  if (!reduceMotion && parallaxEls.length && parallaxConfig.strength > 0) {
    const mobileQuery = window.matchMedia("(max-width: 48rem)");

    const applyParallaxSettings = () => {
      const mobileDisabled = mobileQuery.matches && parallaxConfig.mobileOff;
      parallaxEls.forEach((element) => {
        element.style.setProperty("--parallax-strength", `${parallaxConfig.strength}px`);
        element.style.setProperty("--parallax-scale", String(parallaxConfig.scale));
        const media = element.querySelector(".parallax__media");
        if (!media) return;
        media.style.transform = mobileDisabled ? "none" : "translate3d(0, 0, 0) scale(" + parallaxConfig.scale + ")";
      });
    };

    const updateParallax = () => {
      const viewportHeight = window.innerHeight;
      const mobileDisabled = mobileQuery.matches && parallaxConfig.mobileOff;

      parallaxEls.forEach((element) => {
        const media = element.querySelector(".parallax__media");
        if (!media) return;
        if (mobileDisabled) {
          media.style.transform = "none";
          return;
        }

        const rect = element.getBoundingClientRect();
        const offset = ((viewportHeight - rect.top) / (viewportHeight + rect.height) - 0.5) * parallaxConfig.strength;
        media.style.transform = `translate3d(0, ${offset}px, 0) scale(${parallaxConfig.scale})`;
      });
    };

    let ticking = false;
    const onScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          updateParallax();
          ticking = false;
        });
        ticking = true;
      }
    };

    applyParallaxSettings();
    updateParallax();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", () => {
      applyParallaxSettings();
      updateParallax();
    });
  }

  // Reveal-on-scroll (skipped when the user prefers reduced motion)
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
    window.addEventListener("load", () => navigator.serviceWorker.register(new URL("sw.js", siteRoot), { scope: siteRoot.pathname }).catch(() => {}));
  }
})();
