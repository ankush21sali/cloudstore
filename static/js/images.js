const filters = document.querySelectorAll(".filter-badge");

filters.forEach(btn => {
    btn.addEventListener("click", () => {

        filters.forEach(b => {
            b.classList.remove("active", "filter-dark");
            b.classList.add("filter-light");
        });

        btn.classList.add("active", "filter-dark");
        btn.classList.remove("filter-light");

        const filter = btn.dataset.filter;
        console.log("Filter:", filter);
    });
});