document.querySelectorAll('.fav-btn').forEach(button => {
    button.addEventListener('click', function() {
        const fileId = this.dataset.id;
        const icon = this.querySelector('i');

        fetch(`/dashboard/favourite_item/${fileId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            }
        })

        .then(response => response.json())
        
        .then(data => {
            if (data.is_favourite) {
                icon.classList.remove('bi-star');
                icon.classList.add('bi-star-fill', 'text-warning');
            } else {
                icon.classList.remove('bi-star-fill', 'text-warning');
                icon.classList.add('bi-star');
            }
        });
    });
});

// CSRF helper
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}