document.addEventListener('DOMContentLoaded', () => {
    const commentForm = document.getElementById('commentForm');

    commentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const commentBody = document.getElementById('commentText').value;
        const submitCommentBtn = document.getElementById('submitCommentButton');
        const comment_csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const movieId = submitCommentBtn.getAttribute('data-movie-id');

        submitCommentBtn.disabled = true;
        submitCommentBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting Comment..';

        try {
            const res = await axios.post('/submit_comment/', {
                comment: commentBody,
                movie_id: movieId,
            }, {
                headers: {
                    'X-CSRFToken': comment_csrfToken,
                    'Content-Type': 'application/json'
                }
            });
            
            document.getElementById('commentText').value = '';
            
            if (res.data.status === 'success') {
                location.reload();
            }
        } catch (e) {
            document.getElementById('commentMessage').innerHTML = `
              <div class="alert alert-danger mt-3">Error: ${e.response?.data?.error || 'Failed to submit comment'}</div>`;
        } finally {
            submitCommentBtn.disabled = false;
            submitCommentBtn.innerHTML = 'Post Comment';
            
            setTimeout(() => {
                document.getElementById('commentMessage').innerHTML = '';
            }, 5000);
        }
    });
});