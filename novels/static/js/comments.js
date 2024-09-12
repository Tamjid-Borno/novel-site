document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript is running');
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



const csrftoken = getCookie('csrftoken'); // Ensure this function is correct


// Function to send AJAX request for like or dislike actions
function sendRequest(url, actionType) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken  // Include the CSRF token in headers
        },
        body: JSON.stringify({})  // Body can be empty or include necessary data
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                console.error('Error response:', text);
                throw new Error('Non-JSON response received');
            });
        }
        return response.json();
    })
    .then(data => {
        // Update the like/dislike counts based on action type
        if (actionType === 'like') {
            document.querySelector('.like-count').textContent = data.like_count;
        } else if (actionType === 'dislike') {
            document.querySelector('.dislike-count').textContent = data.dislike_count;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Ensure code runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Handle like and dislike icons
    document.querySelectorAll('.like-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            sendRequest(url, 'like');  // Send the like request
        });
    });

    document.querySelectorAll('.dislike-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            sendRequest(url, 'dislike');  // Send the dislike request
        });
    });

    // Handle reply button toggle
    document.querySelectorAll('.reply-button').forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            const replyForm = document.getElementById('reply-form-' + commentId);
            if (replyForm) {
                replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
            }
        });
    });

    // Handle comment form submission
    document.getElementById('comment-form')?.addEventListener('submit', function(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Handle successful comment addition, e.g., update UI with new comment
            } else {
                // Handle errors, e.g., show error messages
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Handle options dropdown visibility
    document.querySelectorAll('.options-icon').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default button behavior
            const dropdown = this.nextElementSibling;
            const isVisible = dropdown.style.display === 'block';
            document.querySelectorAll('.options-dropdown').forEach(d => d.style.display = 'none'); // Hide other dropdowns
            dropdown.style.display = isVisible ? 'none' : 'block'; // Toggle visibility
        });
    });

    // Handle bookmark button click
    document.getElementById('bookmark-btn')?.addEventListener('click', function(event) {
        event.preventDefault();
        const novelId = this.getAttribute('data-novel-id');
        fetch("{% url 'bookmark_novel' novel.id %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ novel_id: novelId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Novel bookmarked successfully');
            } else {
                alert(data.message || 'Error bookmarking the novel.');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    
});





