function wishList(slug){
    fetch(`${window.location.origin}/remove-wish/`,{
        method:'POST',
        headers:{'X-Requested-With':'XMLHttpRequest'},
        body:JSON.stringify({slug})
    }).then(res => res.json())
        .then(data => {
            if (data.wish_length === 0){
                window.location.reload()
            }
            document.getElementById(`item_close-${slug}`).remove()
        })
}

addToWish = (slug) => {

}