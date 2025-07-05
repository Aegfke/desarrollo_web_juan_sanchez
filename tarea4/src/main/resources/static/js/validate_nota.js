const validateNumero = (num) => {
    return Number.isInteger(num) && num >= 1 && num <= 7;
}


const agregarNota = () => {
    let form = document.forms["myForm"];
    let nota = parseInt(form["act-note"].value, 10);

    if(validateNumero(nota)) {
        form.submit();
    }
    else {
        return;
    }

}

let noteActBtn = document.getElementById("submit-btn");
noteActBtn.addEventListener("click", agregarNota);