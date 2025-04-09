document.addEventListener('DOMContentLoaded', function () {
    const filterForm = document.getElementById('filter-form');
    const moviesContainer = document.getElementById('movies-container');
    const loadMoreBtn = document.getElementById('load-more');

    if (filterForm) {
        filterForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(filterForm);
            const params = new URLSearchParams(formData);
            params.set('page', '1');

            moviesContainer.innerHTML = '<div class="text-center py-5">Loading...</div>';

            axios.get('', { params: params })
                .then(res => {
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = res.data;
                    moviesContainer.innerHTML = tempDiv.querySelector('#movies-container').innerHTML;

                    const newLoadMoreBtn = tempDiv.querySelector('#load-more');
                    if (newLoadMoreBtn) {
                        loadMoreBtn.dataset.nextPage = newLoadMoreBtn.dataset.nextPage;
                        loadMoreBtn.style.display = 'block';
                    } else {
                        loadMoreBtn.style.display = 'none';
                    }

                    window.history.pushState({}, '', `?${params.toString()}`);
                })
                .catch(e => {
                    console.error("Error loading", e);
                    moviesContainer.innerHTML = '<div class="text-center py-5 text-danger">Error loading movies. Please try again.</div>';
                });
        });
    }

    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function () {
            const button = this;
            const nextPage = button.dataset.nextPage;
            const currentParams = new URLSearchParams(window.location.search);
            currentParams.set('page', nextPage);

            button.disabled = true;
            button.textContent = 'Loading...';

            axios.get('', { params: currentParams })
                .then(res => {
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = res.data;

                    const newMovies = tempDiv.querySelector('#movies-container').innerHTML;
                    moviesContainer.insertAdjacentHTML('beforeend', newMovies);

                    const newLoadMoreBtn = tempDiv.querySelector('#load-more');
                    if (newLoadMoreBtn) {
                        button.dataset.nextPage = newLoadMoreBtn.dataset.nextPage;
                        button.disabled = false;
                        button.textContent = 'Load More';
                    } else {
                        button.style.display = 'none';
                    }
                })
                .catch(e => {
                    console.error('Error loading movies', e);
                    button.disabled = false;
                    button.textContent = 'Error - try again or something';
                });
        });
    }
});