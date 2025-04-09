document.addEventListener('DOMContentLoaded', function(){
    const loadMoreButton = document.getElementById('load-more')
    loadMoreButton.addEventListener('click', function(){
        const nextPage = parseInt(this.getAttribute('data-next-page'))
        this.disabled = true;
        this.textContent='Loading..'
        const button = this

        axios.get('/', {
            params:{
                page:nextPage,
                sort_by: '{{ request.GET.sort_by|default:"popularity.desc" }}',
                genre: '{{ request.GET.genre|default:"" }}',
            }
        })
        .then(res=>{
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML=res.data;
            const newMovies = tempDiv.querySelector('#movies-container').innerHTML;
            const newNextPage=tempDiv.querySelector('#load-more').dataset.nextPage

            document.getElementById('movies-container').insertAdjacentHTML('beforeend', newMovies);

            button.dataset.nextPage = newNextPage;

            button.disabled = false;
            button.textContent = 'Load More';
            if (newMovies.trim() === '') {
                button.style.display = 'none';
            }

        }).catch(e=>{
            console.error('error loading movies', e)
            button.disabled = false;
            button.textContent = 'Error - Try Again';
        })
    })
})