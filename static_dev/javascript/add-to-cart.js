$(document).on('click','.add-cart', function () {
        
        const qty = document.querySelector('#qty-' + `${this.dataset.id}`).value
        const path = window.location.origin + '/add-to-cart/'
        fetch(`${path}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',

            },
            body: JSON.stringify({'id': this.dataset.id, 'qty': qty})
        }).then(res => res.json())
            .then(data => document.querySelector('#cart_total_count').innerHTML = data.cart_items)
    })



