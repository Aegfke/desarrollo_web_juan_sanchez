

function agrandarImg(img) {

    const img_box = document.getElementById("agrandar-foto");
    const bigger = document.getElementById("foto-grande");
    const fuente = img.source()
    bigger.source = fuente;
    img_box.hidden = false;

}




document.getElementById("imagen-1").addEventListener("click", agrandarImg())