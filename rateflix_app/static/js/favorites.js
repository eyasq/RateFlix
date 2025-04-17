document.addEventListener('DOMContentLoaded', () => {
    const favBtn = document.querySelector('.favorite-btn');
    
    if (favBtn) {
      favBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        const movieId = this.getAttribute('data-movie-id');
        const movieTitle = this.getAttribute('data-movie-title');
        const moviePoster = this.getAttribute('data-movie-poster');
        
        const poster_url = moviePoster.startsWith('http')
  ? moviePoster
  : `https://image.tmdb.org/t/p/w500${moviePoster}`;
        const movieData = {
          api_id: movieId,
          title: movieTitle,
          poster_url: poster_url,
        };
        
        const form = this.closest('form');
        const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
        
        axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
        
        axios.post('/add_to_favorites/', movieData)
          .then(res => {
            console.log("Response:", res.data);
            
            if (res.data.status === 'success') {
              this.classList.add('favorited');
              this.textContent = '★ Favorited';
              console.log('Movie added to favorites successfully!');
            } else if (res.data.status === 'removed') {
              this.classList.remove('favorited');
              this.textContent = '★ Add to Favorites';
              console.log('Movie removed from favorites!');
            }
          })
          .catch(e => {
            console.error("Error:", e);
          });
      });
    }
  });