const filterData = document.getElementById('filter')

// Filter
filterData.addEventListener('change', function (event) {
    event.preventDefault();
    document.querySelector('.loader').style.display = "block"
    document.querySelector('#products-cont').style.display = 'none'

    const qs_search = new URLSearchParams(window.location.search)
    let formData
    
    if(!qs_search.get('ordering') && !qs_search.get('page')){
        formData = new URLSearchParams(new FormData(this)).toString()
    }
    else if(qs_search.get('ordering') && qs_search.get('page')){
        formData = new URLSearchParams(new FormData(this)).toString() + `&ordering=${qs_search.get('ordering')}` + 
        `&page=${qs_search.get('ordering')}`
    }
    else if(qs_search.get('ordering') && !qs_search.get('page')){
        formData = new URLSearchParams(new FormData(this)).toString() + `&ordering=${qs_search.get('ordering')}`
    }
    else if(!qs_search.get('ordering') && qs_search.get('page')){
        formData = new URLSearchParams(new FormData(this)).toString() + `&page=${qs_search.get('page')}`
    }

    
    const href = window.location.origin + window.location.pathname
    fetch(`${href}?${formData}`,{
        headers:{
            'Content-Type':'application/json',
            'X-Requested-With':'XMLHttpRequest'
        }
    }).then(res => res.json())
        .then(data => {
            window.history.pushState(null,null,`?${formData}`)
            document.querySelector('#products-cont').innerHTML = data.products
            document.querySelector('.loader').style.display = "none";
            document.querySelector('#products-cont').style.display = 'block'
        }
    )
})

// Sorting

const sortingData = document.getElementById('id_ordering')

sortingData.addEventListener('change',function(event){
    
    document.querySelector('.loader').style.display = "block"
    document.querySelector('#products-cont').style.display = 'none'

    const href = window.location.origin + window.location.pathname
    let queryParams
    if(window.location.search.length){
        queryParams =  new URLSearchParams(window.location.search + `&ordering=${event.target.value}`)
        
    }else{
        queryParams = new URLSearchParams(`ordering=${event.target.value}`)
    }

    

    fetch(`${href}?${queryParams.toString()}`,{
        headers:{
            'Content-Type':'application/json',
            'X-Requested-With':'XMLHttpRequest'
        }
    }).then(res => res.json())
        .then(data => {
            queryParams.set('ordering',event.target.value)
            window.history.pushState(null,null,`?${queryParams.toString()}`)
            document.querySelector('#products-cont').innerHTML = `${data.products}`
            document.querySelector('.loader').style.display = "none";
            document.querySelector('#products-cont').style.display = 'block'
        })
    
})

// Pagination

// $(document).on('click', '.pgs', function (event) {
//     let qparam
//     const page = event.target.dataset.page
    
//     if (!window.location.search.length) {
//         qparam = new URLSearchParams(`page=${page}`)
        
//     } else {
        
//         if(!(new URLSearchParams(window.location.search)).has('page')){
//             qparam = new URLSearchParams(window.location.search + `&page=${page}`)
//         }else{
//             qparam = new URLSearchParams(window.location.search)
//             qparam.set('page',`${page}`)
            
//             console.log(qparam.toString())
//         }
//     }
//     window.location.replace(window.location.origin + window.location.pathname + `?${qparam.toString()}`)
//     console.log(qparam.toString())
// })