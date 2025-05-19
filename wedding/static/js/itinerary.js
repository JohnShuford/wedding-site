document.addEventListener("DOMContentLoaded", () => {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  }, {
    threshold: 0.1
  });

  const sections = ["itinerary", "ourstory"];
  sections.forEach(section => {
    const rows = document.querySelectorAll(`.${section} .row`);
    rows.forEach(row => observer.observe(row));
  });
});