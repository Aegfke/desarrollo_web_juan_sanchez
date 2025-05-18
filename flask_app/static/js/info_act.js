document.querySelectorAll('.main-container .image-container img').forEach(image => {
    image.onclick = () =>{
        document.querySelector('.agrandar-foto').style.display = 'block';
        document.querySelector('.agrandar-foto img').src = image.getAttribute('src');
    }
});