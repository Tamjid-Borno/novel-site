document.getElementById('view-more-button').addEventListener('click', function() {
    var button = this;
    var page = parseInt(button.getAttribute('data-page')) + 1;

    fetch(`/home/?page=${page}`)
        .then(response => response.text())
        .then(html => {
            var parser = new DOMParser();
            var doc = parser.parseFromString(html, 'text/html');
            var newItems = doc.querySelector('#novel-list').innerHTML;

            if (newItems.trim() === '') {
                button.style.display = 'none'; // Hide the button if no more items
            } else {
                document.querySelector('#novel-list').innerHTML += newItems;
                button.setAttribute('data-page', page);
            }
        })
        .catch(error => console.error('Error loading more items:', error));
});
