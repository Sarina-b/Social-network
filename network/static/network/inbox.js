document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.post_btn').addEventListener('click', create_new_post)
})

function create_new_post(event) {
    event.preventDefault();
    const now = new Date().toLocaleString();
    fetch('/createPost', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            content: document.querySelector('.content_of_post').value,
            date_posted: now
        })
    })
        .then(result => console.log(result))
        .catch(err => console.error("Fetch error:", err));

    document.querySelector('.content_of_post').value = '';
}