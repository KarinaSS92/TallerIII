#|||||| carga de librerias ||||||#
import requests
import urllib
import time
from bs4 import BeautifulSoup

#|||||| variables globales ||||||#
url = "http://opendata.camara.cl/wscamaradiputados.asmx/"

#|||||| legislatura Actual ||||||#
def legislatura():
	url_aux = url+"getLegislaturaActual"
	req = requests.get(url_aux)
	html = BeautifulSoup(req.text,"html.parser")
	id_legislatura = html.id.get_text()
	numero_legislatura = html.id.get_text()
	inicio_legislatura = html.fechainicio.get_text()
	termino_legislatura = html.fechatermino.get_text()
	return {
				"id_legislatura": id_legislatura,
				"numero_legislatura": numero_legislatura,
				"inicio_legislatura": inicio_legislatura,
				"termino_legislatura":termino_legislatura,
				"sesiones": sesiones(int(id_legislatura))
			}

#|||||| sesiones segun la legilatura ||||||#
def sesiones(id):
	sesiones = {}
	url_aux = url+"getSesiones?prmLegislaturaID="+str(id)
	req = requests.get(url_aux)
	html = BeautifulSoup(req.text,"html.parser")
	aSesiones = html.find_all('sesion')
	for i in range(len(aSesiones)):
		var_id = aSesiones[i].id.get_text()
		var_num = aSesiones[i].numero.get_text()
		var_fech = aSesiones[i].fecha.get_text()
		var_fech_ter = aSesiones[i].fechatermino.get_text()
		var_tipo = aSesiones[i].tipo.get_text()
		var_estado = aSesiones[i].estado.get_text()
		sesiones[i]= {	
							'id_sesion': var_id,
							'numero': var_num,
							'fecha': var_fech,
							'fechatermino': var_fech_ter,
							'tipo_proyecto_ley': var_tipo,
							'estado': var_estado,
							'boletines': boletines(int(var_id))
					 }
	return sesiones

#|||||| boletines segun la sesion ||||||#
def boletines(id):
	boletines = {}
	url_aux = url+"getSesionBoletinXML?prmSesionID="+str(id)
	req = requests.get(url_aux)
	html = BeautifulSoup(req.text,"html.parser");
	#asisten = html.asistencia.get_text()
	#cuenta = html.cuenta.get_text()
	orden = html.orden_dia
	#if(orden):
	#	proyecto = html.find_all('proyecto_ley')
	#	si = {}
	#for i in range(len(proyecto)):
	return boletines

#|||||| carga de metodos y procesos varios ||||||#
print legislatura()
#print sesiones(49)
#boletines(3731)
