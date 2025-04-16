document.addEventListener('DOMContentLoaded', function(){
    const recForm = document.getElementById('recForm');
    
    recForm.addEventListener('submit', function(e){
      e.preventDefault();
      
      const recBtn = document.getElementById('recBtn');
      const resultDiv = document.getElementById('recommendation-results');
      const loadingSpinner = document.querySelector('#recommendation-results .spinner-border');
      const aiResDiv = document.getElementById('ai-response');
      
      resultDiv.style.display = 'block';
      loadingSpinner.style.display = 'block';
      aiResDiv.innerHTML = '';
      recBtn.disabled = true;
      recBtn.innerHTML = 'Generating...';
      
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const formData = new FormData(recForm);
      
      console.log('Sending request to /recommend/');
      
      axios.post('/recommend/', formData, {
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(function(res) {
        console.log('Response received:', res);
        loadingSpinner.style.display = 'none';
        
        if (res.data && typeof res.data === 'object' && res.data.recommendations) {
          aiResDiv.innerHTML = res.data.recommendations;
        } else if (typeof res.data === 'string') {
         
          aiResDiv.innerHTML = res.data.recommendations;
        } else {
          aiResDiv.innerHTML = JSON.stringify(res.data);
        }
        recBtn.disabled = false;
        recBtn.innerHTML = 'Get Personalized Recommendations';
      })
      .catch(function(error) {
        console.error('Error:', error);
        loadingSpinner.style.display = 'none';
        
        aiResDiv.innerHTML = '<div class="alert alert-danger">Error getting recommendations. Please try again.</div>';
        recBtn.disabled = false;
        recBtn.innerHTML = 'Get Personalized Recommendations';
      });
    });
  });