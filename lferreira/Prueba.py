# Import libraries
import requests
import urllib
import time
from bs4 import BeautifulSoup

#----------------------------------------------------
#Variables 
#---------------------------------------------------
url = "https://www.camara.cl/camara/diputados.aspx";
req = requests.get(url);

datos_dipu = {};
status_code = req.status_code;
#----------------------------------------------------
#Main
#----------------------------------------------------

#Si la  conexion es correcta
if status_code == 200:
	#Conexion con url
	html = BeautifulSoup(req.text,"html.parser");

	diputados = html.find_all('li',{'class':'alturaDiputado'});

	for i in range(len(diputados)):
		#------------------------------------
		#Obtiene el nombre 
		#------------------------------------
		nombre =  diputados[i].h5.a.get_text();
		cad ='';
		for y in  nombre.split():
			cad= cad+" "+ y;
		nombre= cad ;
		#-------------------------------------
		#Obtiene Region
		#-------------------------------------
		region = diputados[i].ul.a.get_text();
		region = region.split()[1]
		#-------------------------------------
		#Obtiene Distrito
		#-------------------------------------
		ds = diputados[i].find_all('a')
		ds = ds[3].get_text().split()[1]
		#-------------------------------------
		#Obtiene Partido
		#-------------------------------------
		partido= diputados[i].find_all('a')
		partido=partido[4].get_text().split()[1]
		#-------------------------------------
		#Obtiene Imagen
		#-------------------------------------
		#url2 = "https://www.camara.cl"
		#url2= url2 +diputados[i].img['src']
		#imagen = requests.get(url).content
		#file = open("Imagenes/"+str(i)+".jpg", 'wb')
		#with file as handler:
		#	handler.write(imagen)
		#file.close()
		#-------------------------------------
		#Guarda los datos
		#-------------------------------------
		datos_dipu[i] = {'nombre': nombre,'Region':region,'Distrito':ds,'Partido':partido};

	print "Datos Guardados Correctamente";
#Si la conexion falla 
else : 
	print "Status Error %d" %status_code

print datos_dipu