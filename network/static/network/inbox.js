document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.create_post_form').addEventListener('submit', create_new_post)
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
            content: document.querySelector('.content_of_post').value
        })
    }).then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                document.querySelector(".error-message").innerText = data.error;
                return data;
            });
        }else {
            return response.json().then(data => {
                document.querySelector(".error-message").innerText = data.success;
                return data;
            });
        }
    })
        .then(result => console.log(result))
        .catch(err => console.error("Fetch error:", err));

    document.querySelector('.content_of_post').value = '';
}

