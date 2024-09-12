document.addEventListener('DOMContentLoaded', () => {
    function typeWriter(elementId, text, speed) {
        let i = 0;
        const element = document.getElementById(elementId);
        
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }

    const headlineText = "Hello! Welcome to _____ <3";
    const paragraphText = "Hello! Welcome to my website. I'm thrilled to share my collection of light novels and manga with you. Dive into captivating stories and explore new worlds. Whether you're looking for translated Japanese novels, Chinese epics, or Korean tales, we have it all. Enjoy your journey and happy reading!";

    typeWriter('headline', headlineText, 100);
    setTimeout(() => {
        typeWriter('paragraph', paragraphText, 50);
    }, headlineText.length * 100 + 500); // Adjust delay based on headline length
});


document.getElementById('view-more').addEventListener('click', function(event) {
    event.preventDefault();
    let page = this.getAttribute('data-page');
    let url = new URL(window.location.href);
    url.searchParams.set('page', page);

    fetch(url.toString())
        .then(response => response.text())
        .then(html => {
            let tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;
            let newNovels = tempDiv.querySelector('#novel-container').innerHTML;
            document.querySelector('#novel-container').innerHTML += newNovels;
            this.setAttribute('data-page', parseInt(page) + 1);
        });
});

document.getElementById('bookmark-btn').addEventListener('click', function (event) {
    event.preventDefault();  // Prevent the default behavior of the link

    const novelId = this.getAttribute('data-novel-id');
    
    // Make an AJAX request to bookmark the novel
    fetch(`/bookmark/${novelId}/`, {  // Make sure the URL matches your `urls.py` path
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ novel_id: novelId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            // Optionally change the icon to indicate the novel is bookmarked
            const bookmarkIcon = this.querySelector('ion-icon');
            bookmarkIcon.name = bookmarkIcon.name === 'bookmark-outline' ? 'bookmark' : 'bookmark-outline';
        } else {
            alert(data.message || 'Error bookmarking the novel.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


document.querySelectorAll('.rating-stars i').forEach(star => {
    star.addEventListener('click', function() {
        const rating = this.getAttribute('data-rating');
        const url = this.getAttribute('data-url');
        
        console.log('Star clicked:', rating);  // Check if this is logged

        // Send the rating to the server using fetch API
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,  // Pass CSRF token for security
            },
            body: JSON.stringify({ rating: rating })  // Send the rating value in the request body
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    console.error('Error response:', text);  // Log server error response
                    throw new Error('Error: Non-JSON response received');
                });
            }
            return response.json();  // Parse response as JSON
        })
        .then(data => {
            if (data.success) {
                // Update the UI with the new rating value returned from the server
                document.querySelector('.rating-value').textContent = data.new_rating;
                alert('Rating submitted successfully!');
                console.log('New rating value:', data.new_rating);  // Debug: Log new rating
            } else {
                alert('Error submitting rating: ' + (data.error || 'Unknown error.'));
            }
        })
        .catch(error => {
            console.error('Error:', error);  // Log any error in the fetch process
        });
    });
});