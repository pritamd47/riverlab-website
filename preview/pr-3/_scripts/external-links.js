// Open all external links (and mailto:) in a new tab
document.addEventListener("DOMContentLoaded", () => {
  const host = window.location.hostname;
  document.querySelectorAll("a[href]").forEach((a) => {
    const href = a.getAttribute("href");
    if (
      href.startsWith("http") &&
      !href.includes(host)
    ) {
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener noreferrer");
    }
  });
});
