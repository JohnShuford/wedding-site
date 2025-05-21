document.addEventListener("DOMContentLoaded", () => {    
    document.querySelectorAll('.story-thumbnail').forEach(thumbnail => {
        thumbnail.addEventListener('click', async (e) => {
            const storyId = thumbnail.dataset.id;
            console.log("Thumbnail clicked:", storyId);

            const res = await fetch(`/story-entries/${storyId}/`);
            const data = await res.json();

            document.getElementById('modal-img').src = data.image;
            document.getElementById('modal-title').textContent = data.title;
            document.getElementById('modal-subtitle').textContent = data.subtitle;
            document.getElementById('modal-date').textContent = new Date(data.date).toDateString();
            document.getElementById('modal-description').textContent = data.description;

            document.getElementById('modal').classList.remove('hidden');
        });
    });

    document.querySelector('.close-button').addEventListener('click', () => {
        document.getElementById('modal').classList.add('hidden');
    });
});
