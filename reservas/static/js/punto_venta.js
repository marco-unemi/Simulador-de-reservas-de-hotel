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

document.getElementById("id_cantidad").addEventListener("input", function () {
    // Obtener el valor del tiempo ingresado
    var cantidadInput = document.getElementById("id_cantidad");
    var cantidadValue = cantidadInput.value;

    var precioInput = document.getElementById("id_precio");
    var precioValue = precioInput.value;

    // Calcular el total a pagar (suponiendo que hay una tarifa por hora)
    var totalPagar = precioValue * cantidadValue;

    // Actualizar el campo "Total pagar"
    var totalPagarInput = document.getElementById("id_total_pagar");
    totalPagarInput.value = totalPagar.toFixed(2); // Redondear a dos decimales
});

document.getElementById("id_habitacion").addEventListener("change", function () {
    var habitacionId = this.value;
    var clienteInput = document.getElementById("id_cliente");

    // Obtener el cliente asociado a la habitación seleccionada
    fetch(`/obtener_cliente/${habitacionId}/`)
        .then(response => response.json())
        .then(data => {
            clienteInput.value = data.cliente;
            console.log(clienteInput.value)
        })
        .catch(error => {
            console.error('Error al obtener el cliente:', error);
        });
});