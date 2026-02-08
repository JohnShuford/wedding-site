document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("modal");
  const thumbnails = Array.from(document.querySelectorAll(".story-thumbnail"));
  const storyIds = thumbnails.map((t) => t.dataset.id);
  let currentIndex = -1;

  async function openStory(index) {
    if (index < 0 || index >= storyIds.length) return;
    currentIndex = index;
    const storyId = storyIds[index];

    const res = await fetch(`/wedding/story-entries/${storyId}/`);
    const data = await res.json();

    document.getElementById("modal-img").src = data.image;
    document.getElementById("modal-title").textContent = data.title;
    document.getElementById("modal-subtitle").textContent = data.subtitle;
    document.getElementById("modal-date").textContent = new Date(
      data.date
    ).toDateString();
    document.getElementById("modal-description").innerHTML = data.description;

    // Update arrow visibility
    document.getElementById("modal-prev").classList.toggle("invisible", currentIndex === 0);
    document.getElementById("modal-next").classList.toggle("invisible", currentIndex === storyIds.length - 1);

    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    modal.classList.add("hidden");
    document.body.style.overflow = "";
  }

  thumbnails.forEach((thumbnail, i) => {
    thumbnail.addEventListener("click", () => openStory(i));
  });

  document.querySelector(".close-button").addEventListener("click", closeModal);
  document.getElementById("modal-prev").addEventListener("click", () => openStory(currentIndex - 1));
  document.getElementById("modal-next").addEventListener("click", () => openStory(currentIndex + 1));

  // Click outside modal content to close
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });

  // Keyboard navigation
  document.addEventListener("keydown", (e) => {
    if (modal.classList.contains("hidden")) return;
    if (e.key === "Escape") closeModal();
    if (e.key === "ArrowLeft" && currentIndex > 0) openStory(currentIndex - 1);
    if (e.key === "ArrowRight" && currentIndex < storyIds.length - 1) openStory(currentIndex + 1);
  });
});
