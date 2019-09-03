#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import libraries
import requests
import urllib
from bs4 import BeautifulSoup
import time as t
import json
from tqdm import tqdm
	# Legislatura 
	#     |
	# sesiones
	# 	|
	# boletines
	# 	|
	# proyectos
	# 	|
	# votaciones

#----------------------------------------
#Funciones 
#-----------------------------------------


def cargar_url(url):
	req = requests.get(url)
	html = BeautifulSoup(req.text,"html.parser")
	return html
def obtenerLegislatura():
	url= "http://opendata.camara.cl/wscamaradiputados.asmx/getLegislaturaActual"
	html = cargar_url(url)
	id_legislatura = html.legislatura.id.get_text()
	Numero = html.numero.get_text()
	Fecha_inicio = html.fechainicio.get_text()
	Fecha_termino = html.fechatermino.get_text()

	return {"id_legislatura":id_legislatura,"Numero":Numero,"Fecha_inicio":Fecha_inicio,"Fecha_termino":Fecha_termino,"Sesiones":{}}
#Obtener diputado
def obtener_diputado(ape_p,ape_m):
	url = "http://opendata.camara.cl/wscamaradiputados.asmx/getDiputados_Vigentes"
	html = cargar_url(url)
	diputados = html.find_all("diputado")
	id_diputado = "None"
	for i in range(len(diputados)):
		nombre = diputados[i].nombre.get_text().lower()
		apellido_p = diputados[i].apellido_paterno.get_text().lower()
		apellido_m = diputados[i].apellido_materno.get_text().lower()
		if (ape_p == apellido_p and ape_m == apellido_m):
			id_diputado = diputados[i].dipid.get_text()
	return id_diputado
#Obtiene Boletines
def sesion_boletin(id):
	url = "http://opendata.congreso.cl/wscamaradiputados.asmx/getSesionBoletinXML?prmSesionID="+str(id)
	aSesion_Boletin = {}
	html = cargar_url(url)
	orden_dia = html.orden_dia
	if(orden_dia != None):
		proyectos = orden_dia.find_all("proyecto_ley")
		Diputados_favor = {}
		for i in range (len(proyectos)):
			
			id_boletin=proyectos[i].get("boletin")
			ley  =  proyectos[i].get_text().split(".")[0]
			votaciones = proyectos[i].votacion
			#Variables
			Diputados_favor =[]
			Diputados_abstencion = []
			aFavor ={}
			aAbstencion ={}
			resultado = "None"
			
			# #Si existe etiqueta Votaciones
			if(votaciones != None):
			 	resultado = votaciones.get("resultado")
				#Obtiene votaciones positivas
				positivas =  votaciones.a_favor
				for y in positivas:
					if ( y.string != None ):
						Diputados_favor.append(y)
				#Quita el primer dato del arreglo
				Diputados_favor = Diputados_favor[1:]
				#Obtiene id de los diputados que votaron a favor
				for x in range(len(Diputados_favor)):
					apellido_p = Diputados_favor[x].split(" ")[0].lower()
					apellido_m = Diputados_favor[x].split(" ")[1].split(",")[0].lower()
					if ( obtener_diputado(apellido_p,apellido_m) != "None"):
						aFavor[x] = {"id_diputado":obtener_diputado(apellido_p,apellido_m)}

				#Obtiene votaciones abstencion
				if(votaciones.abstencion != None):
					abstencion = votaciones.abstencion
					for y in abstencion :
						if (y.string != None):
							Diputados_abstencion.append(y)
					Diputados_abstencion = Diputados_abstencion[1:]
					for x in range(len(Diputados_abstencion)):
						apellido_p = Diputados_abstencion[x].split(" ")[0].lower()
						apellido_m = Diputados_abstencion[x].split(" ")[1].split(",")[0].lower()
						if ( obtener_diputado(apellido_p,apellido_m) != "None"):
							aAbstencion[x] = {"id_diputado":obtener_diputado(apellido_p,apellido_m)}

			

			#Guarda los datos en diccionario 
			aSesion_Boletin[i]={"id":id_boletin,"Proyecto_Ley":ley,"Resultado":resultado,"Votos":{"Si":aFavor,"No":[],"Abstencion":aAbstencion}}

			#Reinicia el diccionario
			aFavor= {}
			aAbstencion ={}
			aDispensados = {}

	return aSesion_Boletin
#Obtiene legislatura actual
def sesion_Detalle(id):
	url = "http://opendata.camara.cl/wscamaradiputados.asmx/getSesionDetalle?prmSesionID="+str(id)
	aDatos ={}
	html = cargar_url(url)

	id_sesion = html.id.get_text()
	numero    = html.numero.get_text()

	asistencia = html.find_all('asistentesala')

	for i in range(len(asistencia)):

		id_diputado = asistencia[i].dipid.get_text()
		asis  = asistencia[i].asistencia.get_text()
		aDatos[i] = {'id_sesion':id_sesion,'id_diputado':id_diputado,'asistencia':asis}

	return aDatos

#-------------------------------------------------------
#Datos finales
#------------------------------------------------------

aDatos = obtenerLegislatura()  

url ="http://opendata.camara.cl/wscamaradiputados.asmx/getSesiones?prmLegislaturaID="+str(aDatos['id_legislatura'])
html = cargar_url(url)
sesiones = html.find_all('sesion')
aSesion = {}
for i in tqdm(range(len(sesiones))):

	id_sesion = sesiones[i].id.get_text()
	numero    = sesiones[i].numero.get_text()
	fecha     = sesiones[i].fecha.get_text()
	ftermino  = sesiones[i].fechatermino.get_text()
	tipo      = sesiones[i].tipo.get_text()
	estado    = sesiones[i].estado.get_text()

	aSesion[i]={"Id_sesion":id_sesion,"Numero":numero,"Fecha":fecha,"Fecha Termino":ftermino,
					"Tipo":tipo,"Estado":estado,"Boletin":sesion_boletin(id_sesion)}


aDatos['sesiones'] = aSesion


#Guarda los datos en un archivo
with open('datos.json', 'w') as file:
    json.dump(aDatos, file)



