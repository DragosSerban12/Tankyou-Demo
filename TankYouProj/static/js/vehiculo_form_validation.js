document.addEventListener("DOMContentLoaded", () => {

    // Solo aplico la validación al formulario de crear/editar vehículo
    const form = document.querySelector(".vehiculo-form");
    if (!form) {
        return;
    }

    const submitButton = document.querySelector("#submit-boton");

    submitButton.addEventListener("click", function (e) {
       
        e.preventDefault();


        // Quito errores anteriores
        limpiarErrores();

        let valido = true;

        // Campos del formulario
        const matricula = form.querySelector('[name="matricula"]');
        const marca = form.querySelector('[name="marca"]');
        const modelo = form.querySelector('[name="modelo"]');
        const anyo = form.querySelector('[name="anyo_compra"]');
        const color = form.querySelector('[name="color"]');
        const combustible = form.querySelector('[name="tipo_combustible"]');
        const fotos = form.querySelector('[name="fotos"]');

        // Validaciones básicas
        if (!matricula.value.trim()) {
            mostrarError(matricula, "La matrícula es obligatoria");
            valido = false;
        } else if (matricula.value.length < 5) {
            mostrarError(matricula, "La matrícula debe tener al menos 5 caracteres");
            valido = false;
        }

        if (!marca.value.trim()) {
            mostrarError(marca, "La marca es obligatoria");
            valido = false;
        }

        if (!modelo.value.trim()) {
            mostrarError(modelo, "El modelo es obligatorio");
            valido = false;
        }

        if (!color.value.trim()) {
            mostrarError(color, "El color es obligatorio");
            valido = false;
        }

        // Compruebo que el año tenga sentido
        const anyoActual = new Date().getFullYear();
        if (!anyo.value || anyo.value < 1900 || anyo.value > anyoActual) {
            mostrarError(
                anyo,
                "El año debe estar entre 1900 y " + anyoActual
            );
            valido = false;
        }

        // El select no puede ir vacío
        if (!combustible.value) {
            mostrarError(
                combustible,
                "Selecciona un tipo de combustible"
            );
            valido = false;
        }

        // En crear, controlo el número de fotos
        if (fotos) {
            if (fotos.files.length < 4 || fotos.files.length > 10) {
                mostrarError(
                    fotos,
                    "Debes subir entre 4 y 10 fotos"
                );
                valido = false;
            }
        }

        // Si todo está correcto, dejamos que el formulario se envíe
        if (valido) {
            form.submit();
        }
    });

    // Quito el estado de error cuando el usuario vuelve a tocar el campo
    form.querySelectorAll("input, select").forEach(input => {
        input.addEventListener("blur", () => {
            input.classList.remove("is-invalid");
        });
    });

    // Funciones auxiliares

    function mostrarError(input, mensaje) {
        input.classList.add("is-invalid");

        const error = document.createElement("div");
        error.className = "invalid-feedback";
        error.innerText = mensaje;

        input.parentNode.appendChild(error);
    }

    function limpiarErrores() {
        document.querySelectorAll(".invalid-feedback").forEach(e => e.remove());
        document.querySelectorAll(".is-invalid").forEach(i =>
            i.classList.remove("is-invalid")
        );
    }
});
