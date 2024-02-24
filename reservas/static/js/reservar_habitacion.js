const tipoPagoSelect = document.getElementById("id_tipo_pago");
const tarjetaInputContainer = document.getElementById("tarjeta-input-container");

tipoPagoSelect.addEventListener("click", event => {
    event.preventDefault()

    if (tipoPagoSelect.value === "Tarjeta_de_credito") {
        tarjetaInputContainer.style.display = "block";
    } else {
        tarjetaInputContainer.style.display = "none";
    }
});