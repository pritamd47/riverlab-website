document.addEventListener("DOMContentLoaded", () => {
  const hero = document.querySelector("header[data-big]");
  if (!hero) return;

  // Clone the hero as a compact nav – remove data-big so it gets compact styles
  const nav = hero.cloneNode(true);
  nav.removeAttribute("data-big");
  nav.removeAttribute("style");        // strip hero background-image variable
  nav.setAttribute("aria-hidden", "true");
  nav.classList.add("sticky-nav");
  document.body.insertBefore(nav, document.body.firstChild);

  // Sentinel marks the bottom of the hero
  const sentinel = document.createElement("div");
  hero.after(sentinel);

  new IntersectionObserver(([entry]) => {
    nav.classList.toggle("sticky-nav--visible", !entry.isIntersecting);
  }).observe(sentinel);
});
