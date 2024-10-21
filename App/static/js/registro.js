// Función para activar o desactivar el botón dependiendo del checkbox
function toggleSubmitButton() {
    const checkbox = document.getElementById("check");
    const submitButton = document.getElementById("envio");
    submitButton.disabled = !checkbox.checked;
}

// Validación del formulario
function validate() {
    const v1 = document.getElementById("name");
    const v2 = document.getElementById("rut");
    const v3 = document.getElementById("profesion");
    const v4 = document.getElementById("cargo");
    const v5 = document.getElementById("jornada");
    const v6 = document.getElementById("sueldo");
    const v7 = document.getElementById("fecha");
    const v8 = document.getElementById("email");
    const v9 = document.getElementById("descuentos");

    let flag1 = true, flag2 = true, flag3 = true, flag4 = true, flag5 = true, flag6 = true, flag7 = true, flag8 = true, flag9 = true;

    // Validar nombre
    if (v1.value === "") {
        v1.style.borderColor = "red";
        flag1 = false;
    } else {
        v1.style.borderColor = "green";
        flag1 = true;
    }

    // Validar rut
    if (v2.value === "") {
        v2.style.borderColor = "red";
        flag2 = false;
    } else {
        v2.style.borderColor = "green";
        flag2 = true;
    }

    // Validar profesión
    if (v3.value === "") {
        v3.style.borderColor = "red";
        flag3 = false;
    } else {
        v3.style.borderColor = "green";
        flag3 = true;
    }

    // Validar cargo
    if (v4.value === "") {
        v4.style.borderColor = "red";
        flag4 = false;
    } else {
        v4.style.borderColor = "green";
        flag4 = true;
    }

    // Validar jornada
    if (v5.value === "") {
        v5.style.borderColor = "red";
        flag5 = false;
    } else {
        v5.style.borderColor = "green";
        flag5 = true;
    }

    // Validar sueldo
    if (v6.value === "" || isNaN(v6.value)) {
        v6.style.borderColor = "red";
        flag6 = false;
    } else {
        v6.style.borderColor = "green";
        flag6 = true;
    }

    // Validar fecha de nacimiento
    if (v7.value === "") {
        v7.style.borderColor = "red";
        flag7 = false;
    } else {
        v7.style.borderColor = "green";
        flag7 = true;
    }

    // Validar email
    if (v8.value === "") {
        v8.style.borderColor = "red";
        flag8 = false;
    } else {
        v8.style.borderColor = "green";
        flag8 = true;
    }

    // Validar descuentos
    if (v9.value === "") {
        v9.style.borderColor = "red";
        flag9 = false;
    } else {
        v9.style.borderColor = "green";
        flag9 = true;
    }

    // Retorna true solo si todas las validaciones son correctas
    return flag1 && flag2 && flag3 && flag4 && flag5 && flag6 && flag7 && flag8 && flag9;
}

// Manejar la presentación del formulario
document.querySelector("form").onsubmit = function(event) {
    event.preventDefault();  // Evita el envío del formulario si las validaciones no pasan
    if (validate()) {
        // Si todo es válido, permitir el envío del formulario
        this.submit();
    } else {
        alert("Por favor, complete todos los campos obligatorios.");
    }
};

// Escuchar cambios en el checkbox de términos y condiciones
document.getElementById("check").addEventListener("change", toggleSubmitButton);

// Desactivar el botón de enviar inicialmente
toggleSubmitButton();
