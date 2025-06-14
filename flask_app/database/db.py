import pymysql
import json
import math

from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DB_NAME = "tarea2"
DB_USERNAME = "cc5002" #cc5002
DB_PASSWORD = "programacionweb" #programacionweb
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

with open('database/querys.json', 'r') as querys:
	QUERY_DICT = json.load(querys)

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# --- Models ---

class Actividad(Base):
	__tablename__ = 'actividad'

	id = Column(BigInteger, primary_key=True, autoincrement=True)
	comuna_id = Column(BigInteger, ForeignKey('comuna.id'),nullable=False)
	sector = Column(String(100), nullable=True)
	nombre = Column(String(200), nullable=False)
	email = Column(String(100), nullable=False)
	celular = Column(String(15), nullable=True)
	dia_hora_inicio = Column(DateTime, nullable=False)
	dia_hora_termino = Column(DateTime, nullable=True)
	descripcion = Column(String(500), nullable=True)

class Foto(Base):
	__tablename__ = "foto"

	id = Column(BigInteger, primary_key=True, autoincrement=True)
	ruta_archivo = Column(String(300), nullable=False)
	nombre_archivo = Column(String(300), nullable=False)
	actividad_id = Column(BigInteger, ForeignKey('actividad.id'), nullable=False)
	
class Actividad_tema(Base):
	__tablename__ = "actividad_tema"

	id = Column(BigInteger, primary_key=True, autoincrement=True)
	tema = Column(Enum('música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 'juegos', 'baile', 'comida', 'otro'), nullable=False)
	glosa_otro = Column(String(15), nullable=True)
	actividad_id = Column(BigInteger, ForeignKey('actividad.id'), nullable=False)
	


class Contactar_por(Base):
	__tablename__ = "contactar_por"

	id = Column(BigInteger, primary_key=True, autoincrement=True)
	nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
	identificador = Column(String(150), nullable=False)
	actividad_id = Column(BigInteger, ForeignKey('actividad.id'), nullable=False)

class Comuna(Base):
	__tablename__ = "comuna"

	id = Column(BigInteger, primary_key=True, autoincrement=True)
	nombre = Column(String(200), nullable=False)
	region_id = Column(BigInteger, ForeignKey('region.id'), nullable=False)

class Region(Base):
	__tablename__ = "region"

	id = Column(BigInteger, primary_key=True, autoincrement=True)
	nombre = Column(String(200), nullable=False)

#-------comentario

class Comentario(Base):
	__tablename__ = "comentario"

	id = Column(BigInteger, primary_key=True, autoincrement=True)
	nombre = Column(String(80), nullable=False)
	texto = Column(String(300), nullable=False)
	fecha= Column(DateTime, nullable=False)
	actividad_id = Column(BigInteger, ForeignKey('actividad.id'), nullable=False)


#-- querys --

def get_activities(page_size, page):
	session = SessionLocal()
	offset = (page - 1) * page_size
	actividades = session.query(Actividad).limit(page_size).offset(offset).all()
	session.close()
	return actividades

def get_all_activities():
	session = SessionLocal()
	act = session.query(Actividad).all()
	session.close()
	return act

#-----------------GRAPHS-------------------
def get_first_graph():
	session = SessionLocal()
	act = session.query(Actividad.dia_hora_inicio).all()

	contador = {}
	for actividad in act:
		fecha = actividad[0].date()
		if fecha not in contador:
			contador[fecha] = 0
		contador[fecha] += 1
	
	resultado = [
        {"fecha": fecha.strftime("%Y-%m-%d"), "cantidad": cantidad}
        for fecha, cantidad in contador.items()
    ]
	session.close()

	return resultado

def get_second_graph():
	session = SessionLocal()

	tema_counts = session.query(
        Actividad_tema.tema,
        func.count(Actividad_tema.id).label('cantidad')
    ).group_by(Actividad_tema.tema).all()

	resultado = [{"tema": item.tema, "cantidad": item.cantidad} for item in tema_counts]

	session.close()
	return resultado

def get_third_graph():
	session = SessionLocal()

	act_counts = session.query(Actividad.dia_hora_inicio).all()

	count = {}
	resultado = []

	for (inicio,) in act_counts:
		mes_año = inicio.strftime("%m-%Y").capitalize()

		if mes_año not in count:
			count[mes_año] = {
				"mañana": 0,
				"tarde": 0,
				"noche": 0
			}

		hora = inicio.hour

		if 6 <= hora < 12:
			count[mes_año]['mañana'] += 1
		elif 12 <= hora < 18:
			count[mes_año]['tarde'] += 1
		else:
			count[mes_año]['noche'] += 1
		
	for mes_año in count:
		resultado.append({
			"mes_año": mes_año,
			"cantidad": count[mes_año]
		})
	
	session.close()
	return resultado


#---------------------------------------

def get_activity_by_id(id):
	session = SessionLocal()
	act = session.query(Actividad).filter_by(id=id).first()
	session.close()
	return act


def get_comuna_by_id(id):
	session = SessionLocal()
	comuna = session.query(Comuna).filter_by(id = id).first()
	session.close()

	return comuna

def get_activity_id_by_atributes(nombre, email, inicio):
	session = SessionLocal()
	act = session.query(Actividad).filter_by(nombre=nombre,email=email,dia_hora_inicio=inicio).first()
	session.close()
	return act.id

def get_fotos_by_id(id):
	session = SessionLocal()
	fotos = session.query(Foto).filter(Foto.actividad_id == id).all()
	session.close()
	return fotos

def get_one_foto_by_id(id):
	session = SessionLocal()
	foto = session.query(Foto).filter(Foto.actividad_id == id).first()
	session.close()
	if foto == None:
		return None, None
	return foto.ruta_archivo, foto.nombre_archivo

def get_total_act_pages():
	session = SessionLocal()
	pages = session.query(Actividad).count()
	session.close()
	ret = math.ceil(pages / 5)

	return int(ret)

def get_all_act_values(id):
	session = SessionLocal()

	act = session.query(Actividad).filter_by(id=id).first()
	session.close()

	return act.comuna_id, act.sector, act.nombre , act.email, act.celular, act.dia_hora_inicio, act.dia_hora_termino, act.descripcion

def get_tema_by_act_id(id):
	session = SessionLocal()
	tema = session.query(Actividad_tema).filter(Actividad_tema.actividad_id == id).first()
	session.close()

	return tema

def get_all_temas(id):
	session = SessionLocal()
	temas = session.query(Actividad_tema).filter(Actividad_tema.actividad_id == id).all()
	session.close()

	return temas

def get_all_contactos(id):
	session = SessionLocal()
	temas = session.query(Contactar_por).filter(Contactar_por.actividad_id == id).all()
	session.close()

	return temas

def get_comments_by_id(id):
	session = SessionLocal()
	cursor = session.query(Comentario).filter(Comentario.actividad_id == id).all()
	
	comentarios = []
	for comm in cursor:
		comentarios.append({
			"nombre": comm.nombre,
			"texto": comm.texto,
			"fecha": comm.fecha.strftime("%Y-%m-%d %H:%M:%S")
		})
	session.close()
	return comentarios





def create_activity(comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion):
	session = SessionLocal()
	new_activity = Actividad(comuna_id = comuna_id,sector=sector, nombre=nombre, email=email, celular=celular, dia_hora_inicio=dia_hora_inicio, dia_hora_termino=dia_hora_termino, descripcion=descripcion)
	session.add(new_activity)
	session.commit()
	session.close()

def create_tema(tema, glosa_otro, actividad_id):
	session = SessionLocal()
	new_tema = Actividad_tema(tema=tema, glosa_otro=glosa_otro, actividad_id=actividad_id)
	session.add(new_tema)
	session.commit()
	session.close()

def create_contactar_por(nombre, identificador, actividad_id):
	session = SessionLocal()
	new_contacto = Contactar_por(nombre=nombre, identificador=identificador, actividad_id=actividad_id)
	session.add(new_contacto)
	session.commit()
	session.close()

def create_foto(ruta_archivo, nombre_archivo, actividad_id):
	session = SessionLocal()
	new_foto = Foto(ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo, actividad_id=actividad_id)
	session.add(new_foto)
	session.commit()
	session.close()

def create_comentario(actividad_id, nombre, comentario, fecha):
	session= SessionLocal()
	new_comment = Comentario(nombre = nombre, texto = comentario, fecha = fecha, actividad_id = actividad_id)
	session.add(new_comment)
	session.commit()
	session.close()
	

# -- db-related functions --

def register_actividad(comuna, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion):

	create_activity(comuna, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion)
	return True, None

def register_contacto(nombre, identificador, actividad_id):

	create_contactar_por(nombre, identificador, actividad_id)

	return True, None

def register_tema(tema, glosa_otro, actividad_id):

	create_tema(tema, glosa_otro, actividad_id)

	return True, None

def register_comment(id, nombre, comentario, fecha):

	create_comentario(id, nombre, comentario, fecha)

	return True, None


