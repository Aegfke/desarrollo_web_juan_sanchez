import re
import filetype
from datetime import datetime

temas = ['musica','deporte', 'ciencias', 'religion','politica', 'tecnologia', 'juegos','baile', 'comida']

def validate_name(value):
    return value and len(value) <= 200

def validate_temas(value):
    return all(elem in temas for elem in value)

def validate_email(value):
    return "@" in value


def validate_dia_hora_inicio(value):
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M")
        return True
    except ValueError:
        return False


def validate_act_img(conf_img):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}
    for img in conf_img:
        # check if a file was submitted
        if img is None:
            return False

        # check if the browser submitted an empty file
        if img.filename == "":
            return False
        
        # check file extension
        ftype_guess = filetype.guess(img)
        if ftype_guess.extension not in ALLOWED_EXTENSIONS:
            return False
        # check mimetype
        if ftype_guess.mime not in ALLOWED_MIMETYPES:
            return False
    return True

def validate_act(region, comuna, nombre, email, dia_inicio, temas, fotos):
    print(temas)

    return validate_name(nombre) and validate_email(email) and validate_dia_hora_inicio(dia_inicio) and validate_temas(temas) and validate_act_img(fotos)
