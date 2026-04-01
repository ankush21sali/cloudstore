const filter = document.getElementById('filter-bar');

filter.addEventListener('click', (e) => {
    if (e.target.classList.contains('filter-badge')) {

        // remove active from all
        filter.querySelectorAll('.filter-badge').forEach(btn => {
            btn.classList.remove('active');
            btn.classList.add('filter-badge-light');
        });

        // activate clicked
        e.target.classList.add('active');
        e.target.classList.remove('filter-badge-light');
    }
});