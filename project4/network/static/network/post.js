document.addEventListener('DOMContentLoaded', function() {
    //Post button
    document.querySelector('#new-post-form').onsubmit = function(){
        // Get info from
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
            // Create new card
            div = postDiv(post_body);

            // Show post locally
            let new_post = document.querySelector('#posts');
            new_post.prepend(div);

            // Clear post
            document.querySelector('#new-post-form').innerHTML = '';
        });
            



        return false;
    };


    // Load posts
    fetch('/post')
        .then(response => response.json())
        .then(posts => {
            posts.forEach(post => {
                let new_post = document.querySelector('#posts');

                div = postDiv(post.body);

                new_post.append(div);
            });
            
        });

});

function postDiv(body) {
    const div = document.createElement('div');
    div.className = 'card';

    const card_body = document.createElement('div');
    card_body.className = 'card-body';

    // Body of post
    const body_element = document.createElement('p');
    body_element.className = 'card-text'
    body_element.innerHTML = body;

    // Likes TODO: Like on click
    const like_element = document.createElement('a');
    like_element.className = 'btn btn-primary';
    like_element.innerHTML = 'Like';

    card_body.appendChild(body_element);
    card_body.appendChild(like_element);
    div.appendChild(card_body);

    return div;
}