document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('reviewForm');
    
    reviewForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const reviewText = document.getElementById('reviewText').value;
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const submitBtn = reviewForm.querySelector('button[type=submit]');
      const rating = document.querySelector('select[name=rating]').value;
      const movieId = submitBtn.getAttribute('data-movie-id');
      
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting Review..';
      
      try {
        const response = await axios.post('/submit_review/', {
          review: reviewText,
          movie_id: movieId,
          rating: rating
        }, {
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
          }
        });
        
        document.getElementById('reviewText').value = '';
        document.getElementById('reviewMessage').innerHTML = `
          <div class="alert alert-success mt-3">Review submitted successfully!</div>
        `;
        
        if (response.data.status === 'success') {
          location.reload();
        }
        
      } catch (error) {
        document.getElementById('reviewMessage').innerHTML = `
          <div class="alert alert-danger mt-3">Error: ${error.response?.data?.error || 'Failed to submit review'}</div>`;
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Submit Review';
        
        setTimeout(() => {
          document.getElementById('reviewMessage').innerHTML = '';
        }, 5000);
      }
    });
  });