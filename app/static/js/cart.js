
// Limpiar carrito
document.getElementById('clear-cart').addEventListener('click', function () {
    fetch('/cart/clear/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        }
    });
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Opción "Quitar" del carrito
document.querySelectorAll('.remove-from-cart').forEach(button => {
    button.addEventListener('click', function () {
        const productId = this.dataset.productId;

        fetch(`/cart/remove/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
    });
});


// Cambio en el valor "cantidad", 
//actualiza totales y numero de barra superior
function assignQuantityChangeEvents() {
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function () {
            const productId = this.dataset.productId;
            const newQuantity = parseInt(this.value, 10) || 1;

            if (newQuantity <= 0) {
                alert('La cantidad debe ser mayor a 0.');
                this.value = 1;
                return;
            }

            // Actualizamos el carrito en el servidor
            fetch(`/cart/update/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ quantity: newQuantity }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizamos el total de la fila
                    const row = this.closest('tr');
                    const price = parseFloat(
                        row.querySelector('td:nth-child(3)').textContent.replace('$', '').replace(',', ''));
                    const totalCell = row.querySelector('td:nth-child(6)');
                    const newRowTotal = price * newQuantity;
                    totalCell.textContent = `$${newRowTotal.toLocaleString()}`;

                    // Actualizamos el total global
                    const total = Object.values(data.cart).reduce(
                        (sum, item) => sum + item.price * item.quantity, 0
                    );
                    document.querySelector('#cart-total').textContent = `$${total.toLocaleString()}`;

                    // Actualizamos el contador de la barra superior
                    updateCartCounter(data.cart_count);
                }
            });
        });
    });
}

document.querySelectorAll('input[name="quantity"]').forEach(input => {
    input.addEventListener('change', function () {
        const quantity = parseInt(this.value);
        const row = this.closest('tr'); // Obtener la fila actual
        const productId = row.querySelector('.remove-from-cart').getAttribute('data-product-id');
        
        // Verifica que la cantidad sea válida
        if (quantity > 0) {
            updateCart(productId, quantity, row);
        } else {
            alert("La cantidad debe ser mayor a 0.");
            this.value = 1; // Reestablece un valor válido si el input no lo es
        }
    });
});

function updateCart(productId, quantity, row) {
    fetch('/update-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Actualizar el total de la fila
                row.querySelector('td:last-child').textContent = `$${data.item_total.toLocaleString()}`;

                // Actualizar el total general
                document.getElementById('cart-total').textContent = `$${data.total_price.toLocaleString()}`;
                document.getElementById('cart-count').textContent = `${data.quantity.toLocaleString()}`;
            } else {
                alert("No se pudo actualizar el carrito.");
            }
        })
        .catch(error => console.error('Error:', error));
}
