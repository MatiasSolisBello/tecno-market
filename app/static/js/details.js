function openFullscreen(img) {
    const modal = document.getElementById("fullscreenModal");
    const modalImg = document.getElementById("fullscreenImage");
    modal.style.display = "flex";
    modalImg.src = img.src;
}

function closeFullscreen() {
    document.getElementById("fullscreenModal").style.display = "none";
}

document.getElementById("show-form-btn").addEventListener("click", function() {
    // Muestra el formulario de comentarios
    document.getElementById("comment-form").style.display = "block";
    
    // Desplazamiento suave hacia el formulario
    document.getElementById("comment-form").scrollIntoView({
        behavior: "smooth"
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star-rating i');
    const ratingInput = document.getElementById('id_rating');

    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            ratingInput.value = index + 1; // Asigna el valor de rating
            updateStars(index); // Actualiza la visualización de las estrellas
        });
    });

    function updateStars(index) {
        stars.forEach((star, i) => {
            star.classList.toggle('fas', i <= index);  // Estrella llena para rating seleccionado o menor
            star.classList.toggle('far', i > index);   // Estrella vacía para rating superior al seleccionado
        });
    }
});