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
#------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------#
def obtenerLegislatura():
	url= "http://opendata.camara.cl/wscamaradiputados.asmx/getLegislaturaActual"
	html = cargar_url(url)
	id_legislatura = html.legislatura.id.get_text()
	Numero = html.numero.get_text()
	Fecha_inicio = html.fechainicio.get_text()
	Fecha_termino = html.fechatermino.get_text()

	return {"id_legislatura":id_legislatura,"Numero":Numero,"Fecha_inicio":Fecha_inicio,"Fecha_termino":Fecha_termino}
#------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------#
def get_diputados():
	url = "http://opendata.camara.cl/wscamaradiputados.asmx/getDiputados_Vigentes"
	html = cargar_url(url)
	diputados = html.find_all("diputado")
	id_diputado = "None"
	Dic_Diputados = {}
	for i in range(len(diputados)):
		nombre = diputados[i].nombre.get_text().lower()
		apellido_p = diputados[i].apellido_paterno.get_text().lower()
		apellido_m = diputados[i].apellido_materno.get_text().lower()
		id_diputado= diputados[i].dipid.get_text()
		Dic_Diputados[i]={'id_diputado':id_diputado,'apellido_p':apellido_p,'apellido_m':apellido_m}
	return Dic_Diputados
#------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------#
def get_idDiputado(Dic_Diputados,apellido_p,apellido_m):
	id_dipu = 0
	for i in range(len(Dic_Diputados)):
		if(Dic_Diputados[i]['apellido_p'] == apellido_p and Dic_Diputados[i]['apellido_m'] == apellido_m):
			id_dipu = Dic_Diputados[i]['id_diputado']
	return id_dipu
#------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------#
def sesion_boletin(id,Dic_Diputados):
	url = "http://opendata.congreso.cl/wscamaradiputados.asmx/getSesionBoletinXML?prmSesionID="+str(id)
	aSesion_Boletin = {}
	html = cargar_url(url)
	
	orden_dia = html.orden_dia
	objeto_sesion = html.objeto_sesion

	#--------------------------------
	# SI EXISTE ETIQUIETA ORDEN DIA 
	#--------------------------------
	if(orden_dia != None):
		guardar = True
		proyectos = orden_dia.find_all("proyecto_ley")
		cad = " "
		detalle = ""
		Diputados_favor = {}
		for i in range(len(proyectos)):	
			id_boletin=proyectos[i].get("boletin")
			ley  =  proyectos[i].get_text().split(".")[0]
			votaciones = proyectos[i].votacion
			#Variables
			Diputados_favor =[]
			Diputados_abstencion = []
			Diputados_en_contra = []
			aFavor =[]
			aEn_contra=[]
			aAbstencion =[]
			resultado = "None"


			# #Si existe etiqueta Votaciones
			if(votaciones != None):
			 	resultado = votaciones.get("resultado")
			 	#----------------------------------------------------
				#Obtiene votaciones positivas
				#----------------------------------------------------
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
					id_diputado= get_idDiputado(Dic_Diputados,apellido_p,apellido_m)
					aFavor.append(id_diputado)

				#------------------------------------------------------
				#Obtiene votaciones negativas
				#------------------------------------------------------
				if(votaciones.en_contra != None):
					en_contra = votaciones.en_contra
					for y in en_contra :
						if (y.string != None):
							Diputados_en_contra.append(y)
					Diputados_en_contra = Diputados_en_contra[1:]
					for x in range(len(Diputados_en_contra)):
						apellido_p = Diputados_en_contra[x].split(" ")[0].lower()
						apellido_m = Diputados_en_contra[x].split(" ")[1].split(",")[0].lower()
						id_diputado= get_idDiputado(Dic_Diputados,apellido_p,apellido_m)
						aEn_contra.append(id_diputado)	

				#------------------------------------------------------
				#Obtiene votaciones abstencion
				#------------------------------------------------------
				if(votaciones.abstencion != None):
					abstencion = votaciones.abstencion
					for y in abstencion :
						if (y.string != None):
							Diputados_abstencion.append(y)
					Diputados_abstencion = Diputados_abstencion[1:]
					for x in range(len(Diputados_abstencion)):
						apellido_p = Diputados_abstencion[x].split(" ")[0].lower()
						apellido_m = Diputados_abstencion[x].split(" ")[1].split(",")[0].lower()
						id_diputado= get_idDiputado(Dic_Diputados,apellido_p,apellido_m)
						aAbstencion.append(id_diputado)		

				#---------------------------------------------
				#Obtiene detalle
				#---------------------------------------------
				for remove in  proyectos[i].find_all("intervencion_diputado"):
					remove.decompose()
				for remove in proyectos[i].find_all("votacion"):
					remove.decompose()


				detalle = proyectos[i].get_text()


			#Guarda los datos en diccionario 
			aSesion_Boletin[i]={"id":id_boletin,"proyecto_Ley":ley,"detalle":detalle,"votaciones":{"resultado":resultado,"votos":{"si":aFavor,"no":aEn_contra,"abstencion":aAbstencion}}}
			detalle =''
			#Reinicia el diccionario
			aFavor= {}
			aAbstencion ={}
			aDispensados = {}

	return aSesion_Boletin
#-------------------------------------------------------
#Datos finales
#------------------------------------------------------

Dic_Diputados = get_diputados()
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
					"Tipo":tipo,"Estado":estado,"Boletin":sesion_boletin(id_sesion,Dic_Diputados)}

aDatos['sesiones'] = aSesion


#Guarda los datos en un archivo
with open('json/datos.json', 'w') as file:
    json.dump(aDatos, file)



