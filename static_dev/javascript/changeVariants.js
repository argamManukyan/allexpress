const sizes = document.querySelector('#sizeProduct')

sizes.addEventListener('change',function(event){
    event.preventDefault();
    let  queryParams = new URLSearchParams(window.location.search);
    queryParams.set(event.target.name,event.target.value)
    const url = window.location.origin + window.location.pathname + '?' + queryParams.toString()
    window.location.replace(url)
})
