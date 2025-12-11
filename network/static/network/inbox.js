document.addEventListener('DOMContentLoaded', () => {
    // document.querySelector('.create_post_form').addEventListener('submit', create_new_post);
    const follow_btn = document.querySelector('.follow_btn');
    const unfollow_btn = document.querySelector('.unfollow_btn');
    if (follow_btn) {
        follow_btn.addEventListener('click', follow_button);
    }
    if (unfollow_btn) {
        unfollow_btn.addEventListener('click', unfollow_button);
    }
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
        } else {
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

function follow_button() {

    fetch(`/user_info`, {
        method: 'PUT',
        body: JSON.stringify({
            follow: true,
            clicked_user_id: document.querySelector('.follow_btn').dataset.user_id
        })
    }).then(response => response.json())
        .then(result => {
            const follow_btn = document.querySelector('.follow_btn');
            follow_btn.textContent = 'Unfollow';
            follow_btn.classList.remove('follow_btn');
            follow_btn.classList.add('unfollow_btn');
            document.querySelector('.count_followers').textContent = `Followers : ${result.clicked_user_followers}` ;
            document.querySelector('.count_following').textContent =  `Followings : ${result.clicked_user_following}` ;

        })
        .catch(err => console.error(err));

}

function unfollow_button() {
    fetch(`/user_info`, {
        method: 'PUT',
        body: JSON.stringify({
            follow: false,
            clicked_user_id: document.querySelector('.unfollow_btn').dataset.user_id
        })
    }).then(response => response.json())
        .then(result => {
            const follow_btn = document.querySelector('.unfollow_btn');
            follow_btn.textContent = 'Follow';
            follow_btn.classList.remove('unfollow_btn');
            follow_btn.classList.add('follow_btn');
            document.querySelector('.count_followers').textContent = `Followers : ${result.clicked_user_followers}` ;
            document.querySelector('.count_following').textContent =  `Followings : ${result.clicked_user_following}` ;

        })
        .catch(err => console.error(err));


}

