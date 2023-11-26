document.addEventListener('DOMContentLoaded', function () {
    const celdasExpansibles = document.querySelectorAll('#tabla_dinamica td');

    celdasExpansibles.forEach(celda => {
        celda.addEventListener('click', function () {
            this.classList.toggle('expanded');
        });
    });
});