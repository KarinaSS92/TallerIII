import requests
import urllib
import time as t 
import base64
from bs4 import BeautifulSoup
from tqdm import tqdm

def cargar_url(url):
	req = requests.get(url)
	html = BeautifulSoup(req.text,"html.parser")
	return html

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

def get_idDiputado(Dic_Diputados,apellido_p,apellido_m):
	id_dipu = 0
	for i in range(len(Dic_Diputados)):
		if(Dic_Diputados[i]['apellido_p'] == apellido_p and Dic_Diputados[i]['apellido_m'] == apellido_m):
			id_dipu = Dic_Diputados[i]['id_diputado']
	return id_dipu


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
			aFavor ={}
			aEn_contra={}
			aAbstencion ={}
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
					aFavor[x]={'id_diputado':id_diputado}

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
						aEn_contra[x]= {'id_diputado':id_diputado}		

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
						aAbstencion[x]= {'id_diputado':id_diputado}			

				#---------------------------------------------
				#Obtiene detalle
				#---------------------------------------------
				for remove in  proyectos[i].find_all("intervencion_diputado"):
					remove.decompose()
				for remove in proyectos[i].find_all("votacion"):
					remove.decompose()

				detalle = proyectos[i].get_text()
				print detalle




			#Guarda los datos en diccionario 
			aSesion_Boletin[i]={"id":id_boletin,"proyecto_Ley":ley,"detalle":detalle,"resultado":resultado,"votos":{"si":aFavor,"no":aEn_contra,"abstencion":aAbstencion}}

			#Reinicia el diccionario
			aFavor= {}
			aAbstencion ={}
			aDispensados = {}

	return aSesion_Boletin


Dic_Diputados = get_diputados()


dato = sesion_boletin(3731,Dic_Diputados)
