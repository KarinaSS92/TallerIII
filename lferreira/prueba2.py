import requests
import urllib
import time
import base64
from bs4 import BeautifulSoup

def cargar_url(url):
	req = requests.get(url)
	html = BeautifulSoup(req.text,"html.parser")
	return html


def sesion_boletin(id):
	url = "http://opendata.congreso.cl/wscamaradiputados.asmx/getSesionBoletinXML?prmSesionID="+str(id)
	aSesion_Boletin = {}
	html = cargar_url(url)
	orden_dia = html.orden_dia
	proyectos = orden_dia.find_all("proyecto_ley")

	Diputados_favor = {}

	for i in range (len(proyectos)):
		id_boletin=proyectos[0].get("boletin")
		ley  =  proyectos[0].get_text().split(".")[0]
		votaciones = proyectos[0].votacion
		positivas =  votaciones.a_favor
		#Variables

		aAbstencion ={}




		#Reinicia el diccionario
		aFavor= {}
		aAbstencion ={}
		aDispensados = {}
	
	return aSesion_Boletin


print sesion_boletin(3731)