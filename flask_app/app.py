from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_cors import cross_origin
from utils.validations import validate_act, validate_act_img, validate_comment
from database import db
from werkzeug.utils import secure_filename
from datetime import datetime
import hashlib
import filetype
import os

UPLOAD_FOLDER = 'static/media'

app = Flask(__name__)


app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# --- Routes ---

# ----PORTADA
@app.route("/", methods=["GET"])
def index():
    
    # get last activities
    data = []
    for act in db.get_activities(page_size=5, page=1):
        id = act.id
        comuna_id = act.comuna_id
        comuna = db.get_comuna_by_id(comuna_id)
        sector = act.sector
        nombre = act.nombre
        email = act.email
        celular = act.celular
        dia_hora_inicio = act.dia_hora_inicio
        dia_hora_termino = act.dia_hora_termino
        ruta_archivo, nombre_archivo= db.get_one_foto_by_id(id)
        temas = db.get_all_temas(id) #ARREGLAR-------------------------------
        tema = temas[0]
        
        ### CHECKPOINT 

        img_filename = f"media/{nombre_archivo}"
        data.append({
            "inicio": nombre,
            "hora_inicio": dia_hora_inicio,
            "hora_termino": dia_hora_termino,
            "comuna": comuna.nombre,
            "sector": sector,
            "tema": tema.tema,
            "path_foto": url_for('static', filename=img_filename)
        })
    
    return render_template("html/index.html", data=data) # CAMBIAR


# __FORMULARIO
@app.route("/post-act", methods=["POST","GET"])
def nueva_act():
    if request.method == "POST":
        region = request.form.get("select-region")
        comuna = request.form.get("select-comuna")
        nombre = request.form.get("nombre")
        sector = request.form.get("sector")
        email = request.form.get("email")
        celular = request.form.get("celular")
        contactos = request.form.getlist("contacto")
        inicio = request.form.get("tiempo-inicio")
        fin = request.form.get("tiempo-final")
        descripcion = request.form.get("descripcion")
        temas = request.form.getlist("temas")
        act_img = request.files.getlist("files")
        error = ""
        print(comuna)

        if validate_act(region, comuna, nombre, email, inicio, temas, act_img):

            # 1 save activity in db
            status, msg = db.register_actividad(comuna, sector, nombre, email, celular, inicio, fin, descripcion)
            id = db.get_activity_id_by_atributes(nombre, email, inicio)

            #error += msg 

            # 2 save contactos in db
            for nombre_c in contactos:
                id_formulario = f"{nombre_c}-id"
                identificador = request.form.get(id_formulario)
                status, msg = db.register_contacto(nombre_c,
                                    identificador,
                                    id)

            # 3 save img as file
            for image in act_img:
                _filename = hashlib.sha256(
                    secure_filename(image.filename) # nombre del archivo
                    .encode("utf-8")
                    ).hexdigest()
                _extension = filetype.guess(image).extension
                img_filename = f"{_filename}.{_extension}"

                image.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))

                db.create_foto(app.config["UPLOAD_FOLDER"], img_filename, id)

            # 4 save temas in db
            for t in temas:
                if t == 'otro':
                    otro_tema = request.form.get('otro-id')
                    db.register_tema(t, otro_tema, id)
                    continue
                db.register_tema(t, None, id)
            
            return redirect(url_for("index"))
        else:
            error = "Uno de los campos no es valido."
        
        print(error)

        return render_template("html/nueva_act.html", error=error)
    
    elif request.method == "GET":

        return render_template("html/nueva_act.html", error=None)

#________LISTAS
@app.route("/lista_act", methods = ["GET"])
def lista_act():
    page = int(request.args.get('page', 1))
    total_pages = db.get_total_act_pages()
    
    data = []
    for act in db.get_activities(page_size=5, page=page):
        id = act.id
        comuna_id = act.comuna_id
        comuna = db.get_comuna_by_id(comuna_id)
        sector = act.sector
        nombre = act.nombre
        email = act.email
        celular = act.celular
        dia_hora_inicio = act.dia_hora_inicio
        dia_hora_termino = act.dia_hora_termino
        fotos = db.get_fotos_by_id(id)
        tema = db.get_tema_by_act_id(id)

        tema_nombre = tema.tema

        tema_otro = tema.glosa_otro

        if tema_nombre == 'otro':
            tema_nombre = tema_otro

        img_filenames = []
        for f in fotos:
            nombre_archivo = f.nombre_archivo
            img_filenames.append(url_for('static', filename=f"media/{nombre_archivo}"))
        
        ### CHECKPOINT 

        img_filename = f"media/{nombre_archivo}"
        data.append({
            "id": id,
            "inicio": dia_hora_inicio,
            "termino": dia_hora_termino,
            "comuna": comuna.nombre,
            "sector": sector,
            "tema": tema_nombre,
            "nombre": nombre,
            "imagenes": img_filenames
        })
    
    return render_template("html/lista_act.html", data=data, page=page, total_pages=total_pages)


#INFO
@app.route("/lista_act/info_act/<int:id>", methods = ["GET"])
def info_act(id):
    # get last activity

    comuna_id, sector, nombre, email, celular, inicio, termino, descripcion = db.get_all_act_values(id)

    comuna = db.get_comuna_by_id(comuna_id).nombre

    fotos = db.get_fotos_by_id(id)

    temas= db.get_all_temas(id)

    contactos = db.get_all_contactos(id)

    data_fotos = []

    for f in fotos:
        data_fotos.append(url_for('static', filename=f"media/{f.nombre_archivo}"))

    data = {
        "id": id,
        "comuna": comuna,
        "sector": sector,
        "nombre": nombre,
        "email": email,
        "celular": celular,
        "inicio": inicio,
        "final": termino,
        "descripcion": descripcion,
        "fotos": data_fotos,
        "temas": [t.glosa_otro if t.tema == "otro" else t.tema for t in temas],
        "contactos": contactos 
    }

    return render_template("html/info_act.html", data=data, error=None)
    

@app.route("/get-comment/<int:act_id>", methods=["GET"])
@app.route("/get-comment/", methods=["GET"])
def get_comments(act_id):
    #Obtener los comentarios de una actividad en particular
    ret = db.get_comments_by_id(act_id)

    return jsonify(ret)

@app.route("/post-comment/<int:act_id>", methods=["POST"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def post_comment(act_id):

    data = request.json
    nombre = data.get('nombre')
    texto = data.get('texto')

    if validate_comment(nombre, texto):

            #save comment in db

            fecha = datetime.now()

            db.register_comment(act_id, nombre, texto, fecha)

            return jsonify({"status": "ok", "data": {
                "nombre": nombre,
                "texto": texto,
                "fecha": fecha.strftime("%d/%m/%Y %H:%M:%S")
            }})
    
    else:

        return jsonify({"status": "error", "data": "Invalid comment"}), 400




    



    
    
#-----STATS------------

@app.route("/estadisticas", methods = ["GET"])
def estadisticas():
    return render_template("html/estadisticas.html")

@app.route("/get-stats-data", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def get_stats_data():

    graph1 = db.get_first_graph()

    graph2 = db.get_second_graph()

    graph3 = db.get_third_graph()

    resultado = {
        "graph1": graph1,
        "graph2": graph2,
        "graph3": graph3
    }


    return jsonify(resultado)



if __name__ == "__main__":
    app.run(debug=True)
