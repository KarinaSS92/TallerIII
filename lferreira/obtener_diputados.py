import time as t
import json
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import json


def cargar_url(url):
	req = requests.get(url)
	html = BeautifulSoup(req.text,"html.parser")
	return html


url = "http://opendata.camara.cl/wscamaradiputados.asmx/getDiputados_Vigentes"
html = cargar_url(url)

diputado = html.find_all('diputado')
diputados={}

for i in tqdm(range(len(diputado))):
	#---------------------
	# Datos de diputados
	#---------------------
	id_dipu = diputado[i].dipid.get_text()
	nombre  = diputado[i].nombre.get_text()
	ape_mat = diputado[i].apellido_materno.get_text()
	ape_pa  = diputado[i].apellido_paterno.get_text()
	f_naci  = diputado[i].fecha_nacimiento.get_text()


	diputados[i] = {'id_diputado':id_dipu,'nombre':nombre,'apellido_paterno':ape_pa,'apellido_materno':ape_mat,'fecha_nacimiento':f_naci}


with open('json/diputados.json', 'w') as file:
    json.dump(diputados, file)