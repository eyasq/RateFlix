document.addEventListener('DOMContentLoaded', function() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            // data = name
            const movieId = this.getAttribute('data-movie-id');
            const movieTitle = this.getAttribute('data-movie-title');
            const moviePoster = this.getAttribute('data-movie-poster');
            
            // this object, we will send data to the backend using it
            const movieData = {
                api_id: movieId,
                title: movieTitle,
                poster_url: moviePoster ? `https://image.tmdb.org/t/p/w500${moviePoster}` : null
            };
            
            // grab csrf token so request isnt denied by django
            const form = this.closest('form');
            const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
            
            // add it to axios
            axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
            
            // make an xios post req
            axios.post('/add_to_favorites/', movieData)
                .then(response => {
                    // if success
                    if (response.data.status === 'success') {
                        // Change button appearance to indicate the movie is now favorited
                        this.classList.add('favorited');
                        this.textContent = '★ Favorited';
                        
                        // debug
                        console.log('Movie added to favorites successfully!');
                    } else if (response.data.status === 'removed') {
                        // if success, but already added, remove
                        this.classList.remove('favorited');
                        this.textContent = '★ Add to Favorites';
                        
                        console.log('Movie removed from favorites!');
                    }
                })
                .catch(error => {
                    console.error('Error adding movie to favorites:', error);
                    
                    if (error.response && error.response.data.error) {
                        console.error(error.response.data.error);
                    }
                });
        });
    });
});

