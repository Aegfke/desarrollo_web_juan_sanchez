const validateName = (name) => {
    if(!name) return false;
    let lengthValid = name.trim().length <= 80 && name.trim().length >= 3;

    return lengthValid;
}

const validateComment = (comment) => {
    if(!comment) return false;

    let lengthValid = comment.trim().length >= 5;

    return lengthValid;
}

const validateAll = () => {
    

    let form = document.forms["comments"];
    let nombre = form["nombre"].value;
    let comentario = form["comentario"].value;
    let actividad_id = form.dataset.actividadId;

    let validationBox = document.getElementById("val-box");
    let validationMessageElem = document.getElementById("val-msg");
    let validationListElem = document.getElementById("val-list");

    let isValid = validateComment(comentario) && validateName(nombre);

    if (isValid) {
        validationBox.hidden = true;
        validationListElem.textContent = "";
        commentActivity(actividad_id, nombre, comentario);
    }
    else {
        validationListElem.textContent = "";
        validationMessageElem.innerText = "El comentario es invalido:";
        if (!validateComment(comentario)) {
            const listElement = document.createElement("li");
            listElement.innerText = "Comentario no válido";
            validationListElem.appendChild(listElement);
        };
        if (!validateName(nombre)) {
            const listElement = document.createElement("li");
            listElement.innerText = "Nombre no válido";
            validationListElem.appendChild(listElement);
        }

        validationBox.style.backgroundColor = "#ffdddd";
        validationBox.style.borderLeftColor = "#f44336";

        validationBox.hidden = false;
    }

};

const agregarComentario = (comentario) => {
    const comment_div = document.getElementById("comment_list");

    const new_div = document.createElement('div');
    new_div.className = 'comentario';
    new_div.innerHTML = `<b>${comentario.nombre}:</b><p>${comentario.texto}</p><br><p>${comentario.fecha}</p>`;

    comment_div.appendChild(new_div);

};



const commentActivity = (act_id, nombre, texto) => {
    const form = document.forms["comments"];
    fetch(`${window.origin}/post-comment/${act_id}`, {
        method: "POST",
        body: JSON.stringify({
            nombre: nombre,
            texto: texto
        }),
        credentials: "include",
        cache: "no-cache",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
            if (!response.ok) {
                validationBox.hidden = false;
                validationMessageElem.innerText = "Comentario Invalido";
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            agregarComentario(data.data); // Agregar nuevo comentario
            form.reset();
        })
        .catch((error) => {
            console.error(
                "There has been a problem with your fetch operation:",
                error
            );
        });
};

const fetchComments = async (url) => {

    fetch(url, {
        mode: "cors",
        credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((commentJs) => {
        commentJs.forEach(comentario => agregarComentario(comentario));
        console.log(commentJs);
      })
      .catch((error) => {
        console.error(
            "There has been a problem with your fetch operation:",
            error
        );
      });
};

let form = document.forms["comments"];
let actividad_id = form.dataset.actividadId;

window.onload = () => {
    fetchComments(fetchComments(`${window.origin}/get-comment/${actividad_id}`));
}

let submitAct = document.getElementById("submit-comment");
submitAct.addEventListener("click", validateAll);