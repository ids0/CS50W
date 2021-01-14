document.addEventListener('DOMContentLoaded', function() {
    //Post button
    document.querySelector('#new-post-form').onsubmit = function(){
        // Get post body from form
        post_body = document.querySelector('#post-body').value;

        // Create request with CSRF Token in header
        const request = new Request(
            '/post',
            { headers: { 'X-CSRFToken': CSRF_TOKEN } }
        );
        // TODO: Error handling
        // POST request to server with request
        fetch(request, {
            method:'POST',
            mode: 'same-origin',
            body:JSON.stringify({
                body:post_body
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);

            // TODO: Update this Show post locally
            // Maybe fetch post from server?


            // Create new card
            div = newPost(post_body);

            let new_post = document.querySelector('#recent-post');
            new_post.prepend(div);

            // TODO: Animation

            // Clear post
            document.querySelector('#post-body').value = '';
        });
            
        return false;
    };

    let actual_page = 1;

    // Load Page 1
    loadPosts(actual_page);

    // Previous / Next Buttons
    document.querySelector('#next-page').onclick = function(){
        actual_page++;
        loadPosts(actual_page);


        return false;
    }
    document.querySelector('#previous-page').onclick = function () {
        actual_page--;
        if (actual_page <= 0){
            actual_page = 1;
        }
        loadPosts(actual_page);
        return false;
    }

});


function loadPosts(page_number) {

    // Clear old posts
    document.querySelector('#posts').innerHTML = '';

    // Load posts
    fetch(`/post/${page_number}`)
        .then(response => response.json())
        .then(response_object => {
            // Prev/Nex buttons
            if (page_number === 1) {
                document.querySelector('#previous-page').parentElement.classList.add("disabled");
            } else {
                document.querySelector('#previous-page').parentElement.classList.remove("disabled");
            }

            if (page_number === response_object.pages) {
                document.querySelector('#next-page').parentElement.classList.add("disabled");
            } else {
                document.querySelector('#next-page').parentElement.classList.remove("disabled");
            }

            response_object.posts.forEach(post => {
                div = postDiv(post);


                const new_post = document.querySelector('#posts');
                new_post.append(div);
            });
        });
    return true;
}

function newPost(body) {

    // Create post object for postDiv
    const post = {
        id:-1,
        user: current_user,
        time:"Now",
        body:body,
        likes:0,
    };

    return postDiv(post);
}

function postDiv(post) {
    const div = document.createElement('div');
    div.className = 'card border-secondary mb-3';
    div.style = 'max-width: 56rem;'

    // TODO: Add user and time
    const card_body = document.createElement('div');
    card_body.className = 'card-body text-dark';

    // Post's body
    const body_element = document.createElement('p');
    body_element.id = "posts-body"
    body_element.className = 'card-text'
    body_element.innerHTML = post.body;
    card_body.appendChild(body_element);

    // Likes
    const like_element = document.createElement('a');
    like_element.className = 'btn btn-primary';
    like_element.innerHTML = post.likes;
    if (post.liked) {
        like_element.innerHTML = `♥ : ${post.likes}`;
    } else {
        like_element.innerHTML = post.likes;
    }

    like_element.onclick =  function () {
        // If user is not post owned
        if (!post.owned){
            // Change local state
            post.liked = !post.liked;
            // Request with token
            const request = new Request(
                '/post',
                { headers: { 'X-CSRFToken': CSRF_TOKEN } }
            );
            // PUT request with updated status
            fetch(request, {
                method: 'PUT',
                body: JSON.stringify({
                    reason: 'Like',
                    id: post.id,
                    liked: post.liked
                })
            });
            // Change local info
            if (post.liked) {
                post.likes++;
                like_element.innerHTML = `♥ : ${post.likes}`;
            } else {
                post.likes--;
                like_element.innerHTML = post.likes;
            }
        }
    };

    card_body.appendChild(like_element);

    // User
    const user_element = document.createElement('a');
    user_element.className = 'label success text-right';
    user_element.innerHTML = post.user;
    user_element.href = `/user/${post.user}`;
    card_body.appendChild(user_element);

    // time
    const time_element = document.createElement('span');
    time_element.className = 'label success text-right';
    time_element.innerHTML = post.time;
    card_body.appendChild(time_element);

    // Edit
    if (post.owned) {
        const edit_element = document.createElement('a');
        edit_element.innerHTML = "edit";
        edit_element.href = `#`;
        edit_element.onclick = function () {
            // Get element to edit
            const post_to_edit = edit_element.parentNode.childNodes[0];
            // Save post body
            let post_body = post_to_edit.textContent;
            // Create new element
            const edit_post_form = document.createElement('form');
            edit_post_form.id = 'edit-post-form';
            // Create textarea
            const text_box = document.createElement('textarea');
            text_box.id = "posts-body";
            text_box.value = post_body;
            edit_post_form.appendChild(text_box);
            // Create save button
            const save_button = document.createElement('input');
            save_button.type = 'submit';
            save_button.value = 'Save'
            edit_post_form.appendChild(save_button);

            // Onsubmit edit post on server and locally
            edit_post_form.onsubmit = function () {
                // new post body
                post_body = text_box.value


                // Update server
                const request = new Request(
                    '/post',
                    { headers: { 'X-CSRFToken': CSRF_TOKEN } }
                );

                // PUT request with reason,id and body
                fetch(request, {
                    method: 'PUT',
                    body: JSON.stringify({
                        reason:'Update',
                        id: post.id,
                        body: post_body
                    })
                });

                // Update localy
                post_to_edit.textContent = text_box.value;
                edit_element.parentNode.replaceChild(post_to_edit, edit_post_form);

                return false;
            }
            // Replace Element
            edit_element.parentNode.replaceChild(edit_post_form, post_to_edit);

        }
        card_body.appendChild(edit_element);
    }
    


    div.appendChild(card_body);

    return div;
}

