const validateName = (name) => {
    if(!name) return false;
    let lengthValid = name.trim().length <= 200;

    return lengthValid;
}

const validatePhoneNumber = (phoneNumber) => {
    if (!phoneNumber) return true;
    // validación de longitud
    let lengthValid = phoneNumber.length >= 8;
  
    // validación de formato
    let re = /^[0-9]+$/;
    let formatValid = re.test(phoneNumber);
  
    // devolvemos la lógica AND de las validaciones.
    return lengthValid && formatValid;
  };

const validateEmail = (email) => {
    if (!email) return false;
    let lengthValid = email.length < 100;

    let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
    let formatValid = re.test(email);

    return lengthValid && formatValid;
};

const validateSelect = (select) => {
    if(!select) return false;
    return true;
}

const validateFiles = (files) => {
    if (files.length == 0) return false;
  
    // validación del número de archivos
    let lengthValid = 1 <= files.length && files.length <= 5;
  
    // validación del tipo de archivo
    let typeValid = true;
  
    for (const file of files) {
      // el tipo de archivo debe ser "image/<foo>" o "application/pdf"
      let fileFamily = file.type.split("/")[0];
      typeValid &&= fileFamily == "image" || file.type == "application/pdf";
    }
  
    // devolvemos la lógica AND de las validaciones.
    return lengthValid && typeValid;
};

const validateCheckBoxContact = (boxes) => {
    let selected = 0;
    for (const b of boxes) {
        if (b.checked) {
            selected++;
        }
    }
    return selected <= 5;
}

const validateCheckBoxSubjectMin = (boxes) => {

    let selected = 0;
    for (const b of boxes) {
        if (b.checked) {
            selected++;
        }
    }
    return selected >= 1;
}

const validateIHour = (hour) => {
    if (!hour) return false;
    const ahora = new Date();
    const hourSelected = new Date(hour);
    if (hourSelected < ahora) {
        return false;
    }
    return true;

}

const validateFHour = (hour) => {
    if (!hour) return true;
    const inicio = new Date(document.getElementById("tiempo-inicio").value);
    const hourSelected = new Date(hour);
    if (hourSelected < inicio) {
        return false;
    }
    return true
}

const validateForm = () => {

    let myForm = document.forms["myForm"];
    let region = myForm["select-region"].value;
    let comuna = myForm["select-comuna"].value;
    let nombre = myForm["nombre"].value;
    let celular = myForm["celular"].value;
    let email = myForm["email"].value;
    let contacto = myForm.querySelectorAll('.form-sect2 input[type="checkbox"]');
    let tiempoInicial = myForm["tiempo-inicio"].value;
    let tiempoFinal = myForm["tiempo-final"].value;
    let tema = myForm.querySelectorAll('.form-sect3 input[type="checkbox"]');
    let filesInput = myForm.querySelectorAll('#contenedor-files input[type="file"]');

    let files = [];
    for (const input of filesInput) {
        const fileList = input.files;
        for (const file of fileList) {
            files.push(file);
        }
    }

    let invalidInputs = [];
    let isValid = true;
    const setInvalidInput = (inputName) => {
        invalidInputs.push(inputName);
        isValid &&= false;
    }

    if (!validateSelect(region)) {
        setInvalidInput("Región");
    }
    if (!validateSelect(comuna)) {
        setInvalidInput("Comuna");
    }
    if (!validateName(nombre)) {
        setInvalidInput("Nombre");
    }
    if (!validateEmail(email)) {
        setInvalidInput("Email");
    }
    if (!validatePhoneNumber(celular)) {
        setInvalidInput("Celular(opcional)");
    }
    if (!validateCheckBoxContact(contacto)) {
        setInvalidInput("Contacto");
    }
    if (!validateCheckBoxSubjectMin(tema)) {
        setInvalidInput("Número de temas");
    }
    if (!validateIHour(tiempoInicial)) {
        setInvalidInput("Hora de inicio");
    }
    if (!validateFHour(tiempoFinal)) {
        setInvalidInput("Hora final(opcional)")
    }
    if (!validateFiles(files)) {
        setInvalidInput("Archivos");
    }

    let validationBox = document.getElementById("val-box");
    let validationMessageElem = document.getElementById("val-msg");
    let validationListElem = document.getElementById("val-list");
    let formContainer = document.querySelector(".main-container");

    if (!isValid) {
        validationListElem.textContent = "";
        // agregar elementos inválidos al elemento val-list.
        for (input of invalidInputs) {
            let listElement = document.createElement("li");
            listElement.innerText = input;
            validationListElem.append(listElement);
        }
        // establecer val-msg
        validationMessageElem.innerText = "Los siguientes campos son inválidos:";

        // aplicar estilos de error
        validationBox.style.backgroundColor = "#ffdddd";
        validationBox.style.borderLeftColor = "#f44336";

        // hacer visible el mensaje de validación
        validationBox.hidden = false;
    } else {
        // Ocultar el formulario
        myForm.style.display = "none";

        // establecer mensaje de éxito
        validationMessageElem.innerText = "¿Está seguro que desea agregar esta actividad?";
        validationListElem.textContent = "";

        // aplicar estilos de éxito
        validationBox.style.backgroundColor = "#ddffdd";
        validationBox.style.borderLeftColor = "#4CAF50";

        // Agregar botones para enviar el formulario o volver
        let submitButton = document.createElement("button");
        submitButton.innerText = "Sí, estoy seguro";
        submitButton.style.marginRight = "10px";
        submitButton.addEventListener("click", () => {
            validationMessageElem.innerText = "Hemos recibido su información, muchas gracias y suerte en su actividad";
            submitButton.innerText = "Volver a la portada";
            backButton.remove();
            submitButton.addEventListener("click", () => {
                window.location.href = '/html/index.html';
            });
        });

        let backButton = document.createElement("button");
        backButton.innerText = "No, no estoy seguro, quiero volver al formulario";
        backButton.addEventListener("click", () => {
            // Mostrar el formulario nuevamente
            myForm.style.display = "block";
            validationBox.hidden = true;
        });

        validationListElem.appendChild(submitButton);
        validationListElem.appendChild(backButton);

        // hacer visible el mensaje de validación
        validationBox.hidden = false;
    }
};

let submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener("click", validateForm);
