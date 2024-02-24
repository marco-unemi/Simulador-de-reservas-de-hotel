document.addEventListener("DOMContentLoaded", function () {
    const btnsEditarUsuario = document.querySelectorAll(".btn-editar-usuario");

    btnsEditarUsuario.forEach(btn => {
        btn.addEventListener("click", function (event) {
            event.preventDefault();
            const userId = this.getAttribute("data-user-name");
            const modalBody = document.querySelector("#modalEditarInfoHotel .modal-body");
            modalBody.textContent = "¿Quieres editar al usuario con nombre: " + userId + " ?";
        });
    });
});