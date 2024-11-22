function openFullscreen(img) {
    const modal = document.getElementById("fullscreenModal");
    const modalImg = document.getElementById("fullscreenImage");
    modal.style.display = "flex";
    modalImg.src = img.src;
}


function closeFullscreen() {
    document.getElementById("fullscreenModal").style.display = "none";
}


// Mostrar formulario de comentario
document.getElementById("show-form-btn").addEventListener("click", function() {
    document.getElementById("comment-form").style.display = "block";
    
    document.getElementById("comment-form").scrollIntoView({
        behavior: "smooth"
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star-rating i');
    const ratingInput = document.getElementById('id_rating');

    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            ratingInput.value = index + 1;
            updateStars(index);
        });
    });

    function updateStars(index) {
        stars.forEach((star, i) => {
            star.classList.toggle('fas', i <= index);
            star.classList.toggle('far', i > index);
        });
    }
});


// Añadir al carrito
document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function () {
        const productId = this.dataset.productId;
        const quantity = 1;

        fetch(`/cart/add/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ quantity }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let timerInterval;
                Swal.fire({
                title: "Producto añadido al carrito",
                icon: "success",
                timer: 2000,
                timerProgressBar: false,
                willClose: () => {
                    clearInterval(timerInterval);
                    location.reload();
                }
                })/*.then((result) => {
                 Read more about handling dismissals below 
                    if (result.dismiss === Swal.DismissReason.timer) {
                    }
                });*/
            }
        });
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
