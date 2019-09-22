<<<<<<< HEAD:lferreira/Obtener_Etiquetas.py
import pymongo 
import nltk
import nltk.data
import time as t
import sys
import os.path
import json
from pymongo import MongoClient
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding('utf8')

#---------------------------------
# Funciones
#----------------------------------
def get_Sinonimos(text):
	url = "http://www.wordreference.com/sinonimos/"+text
	resp = requests.get(url)
	sinonimos = []
	bs=BeautifulSoup(resp.text,'lxml')
	lista=bs.find_all(class_='trans clickable')
	sin = ['None']
	for i in lista : 
		sin =  i.find_all('li')
	for i in sin : 
		if ( i != 'None') :
			if(i.span == None): 
				for y in i.get_text().split(','):
					sinonimos.append(y.strip())
	return sinonimos
def guardar(Dic):
	with open("Palabras_Final.json",'w') as f:
		json.dump(Dic,f)

def crear_json2():
	with open('Palabras.json','r') as f:
	 file = json.load(f)
	 for i in tqdm(range(len(file)),"Progreso Total"):
	 	id_sesion = file[str(i)]['id_sesion']
	 	boletin   = file[str(i)]['boletin']
	 	pal_new   = []
	 	for y in tqdm(range(len(boletin)),"Obteniendo sinonimos de cada Proyecto"):
	 		id_proyecto =  boletin[str(y)]['id_proyecto']
	 		for pal in boletin[str(y)]['palabras']:
	 			pal_new.append(pal)
	 			try :
					sinonimos = get_Sinonimos(pal)
					for sin in sinonimos:
						pal_new.append(sin)
	 			except requests.exceptions.ConnectionError as err:
	 				log = open('log.txt','w')
	 				cad = "indice_sesion:"+str(i)+",indice_boletin:"+str(y)+",utlima_palabra:"+str(pal)
	 				log.write(cad)
	 				log.close()
	 				guardar(Json_sinonimos)
	 				print err
	 				sys.exit(1)
	 		Dic_Proyectos[y]={'id_proyecto':id_proyecto,'palabras':pal_new}
	 		pal_new = []
	 	Json_sinonimos[i] = {"id_sesion":id_sesion,"boletin":Dic_Proyectos}
	guardar(Json_sinonimos)

def continua_creacion(indice_sesion,indice_boletin,utlima_palabra):
	Json_sinonimos = {}
	with open('Palabras_Final.json') as f:
		Json_sinonimos = json.load(f)
	with open('Palabras.json','r') as f:
			 file = json.load(f)
			 indice_s = len(file)-int(indice_sesion)
			 continua   = False
			 for i in tqdm(range(indice_s),"Progreso Total"):
			 	id_sesion = file[str(i)]['id_sesion']
			 	boletin   = file[str(i)]['boletin']
			 	indice_b  = len(boletin)- int(indice_boletin)
			 	pal_new   = []
			 	for y in tqdm(range(indice_b),"Obteniendo sinonimos de cada Proyecto"):
			 		id_proyecto =  boletin[str(y)]['id_proyecto']
			 		for pal in boletin[str(y)]['palabras']:
			 			pal_new.append(pal)
			 			if(pal == utlima_palabra): continua=True
			 			if (continua == True):
				 			try :
								sinonimos = get_Sinonimos(pal)
								for sin in sinonimos:
									pal_new.append(sin)
				 			except requests.exceptions.ConnectionError as err:
				 				log = open('log.txt','w')
				 				cad = "indice_sesion:"+str(i)+",indice_boletin:"+str(y)+",utlima_palabra:"+str(pal)
				 				log.write(cad)
				 				log.close()
				 				guardar(Json_sinonimos)
				 				print err
				 				sys.exit(1)
			 		Dic_Proyectos[y]={'id_proyecto':id_proyecto,'palabras':pal_new}
			 		pal_new = []
			 	Json_sinonimos[i] = {"id_sesion":id_sesion,"boletin":Dic_Proyectos}
	guardar(Json_sinonimos)
#----------------------------------
#Conexion con mongodb 
#-----------------------------------

def Crear_Json():
	con = MongoClient("Localhost",27017)
	db  = con.parlamento
	#----------------------------------
	#Carga Coleccion 
	#----------------------------------
	quevotan = db.quevotan
	data = quevotan.find_one()
	sesiones = data['sesiones']

	Dic_palabras = {}
	dic_boletin  = {}	
	print "\n \n"
	for i in tqdm(range(len(data['sesiones'])),'Obteniendo Palabras '):
		boletin = sesiones[str(i)]['Boletin']
		for y in range(len(boletin)):
			#----------------------------------
			#Procesamiento de texto con NLTK --
			#----------------------------------
			detalle = boletin[str(y)]['detalle']
			palabras = nltk.word_tokenize(detalle)
			texto    = nltk.Text(palabras)
			corpu    = nltk.corpus.stopwords.words("spanish")
			tags     = nltk.pos_tag(palabras) #Obtiene tags con detalle de la palabra
			fdist = nltk.FreqDist(texto) #Busca palabras que mas se repitan en el texto
			a_tags =[]
			guardar = True
			#print tags
			
			#Quita palabras que contiene variable corpus
			for i2 in tags :
				if(i2[1] == 'NNP' and len(i2[0]) > 2):
					for y2 in range(len(corpu)) : 
						if ( i2[0].lower() == corpu[y2]):
							guardar = False
					if(guardar):
						a_tags.append(i2[0])
					guardar = True

			dic_boletin[y]={'id_proyecto':boletin[str(y)]['id'],'palabras':a_tags}
			#print boletin
		Dic_palabras[i] = {"id_sesion":sesiones[str(i)]['Id_sesion'],"boletin":dic_boletin}

	#-------------------------------------
	# Guarda json con palabras sin los sinonimos
	#---------------------------------------
	with open('Palabras.json', 'w') as file:
	    json.dump(Dic_palabras, file)

	print "Archivo Guardado  \n \n"
#Si el archivo no existe crea json
if ( os.path.isfile('Palabras.json') == False):
	Crear_Json()
else : 
	#Pregunta si el archivo esta vacio 
	with open('Palabras.json','r') as f:
		file = json.load(f)
		if (len(file) == 0 ):
			Crear_Json()
#-------------------------------------
# Cargar Json 
#---------------------------------------

Json_sinonimos = {}
Dic_Proyectos  = {}

#Continua con la creacion del json , carga de la ultima parte que quedo 
if( os.path.isfile('log.txt') == False ) : print "ERROR"
else : 
	file = open('log.txt')
	cad  = file.read().split(',')
	indice_sesion = cad[0].split(':')[1]
	indice_boletin= cad[1].split(':')[1]
	utlima_palabra= cad[2].split(':')[1]
	if (indice_boletin == 'None' and indice_sesion == 'None' and utlima_palabra == 'None'):
		crear_json2()
	else:
		continua_creacion(indice_sesion,indice_boletin,utlima_palabra)



		








=======
import pymongo 
import nltk
import nltk.data
import time as t
import sys
import os.path
import json
from pymongo import MongoClient
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding('utf8')

#---------------------------------
# Funciones
#----------------------------------
def get_Sinonimos(text):
	url = "http://www.wordreference.com/sinonimos/"+text
	resp = requests.get(url)
	sinonimos = []
	bs=BeautifulSoup(resp.text,'lxml')
	lista=bs.find_all(class_='trans clickable')
	sin = ['None']
	for i in lista : 
		sin =  i.find_all('li')
	for i in sin : 
		if ( i != 'None') :
			if(i.span == None): 
				for y in i.get_text().split(','):
					sinonimos.append(y.strip())
	return sinonimos
def guardar(Dic):
	with open("Palabras_Final.json",'w') as f:
		json.dump(Dic,f)

def crear_json2():
	with open('Palabras.json','r') as f:
	 file = json.load(f)
	 for i in tqdm(range(len(file)),"Progreso Total"):
	 	id_sesion = file[str(i)]['id_sesion']
	 	boletin   = file[str(i)]['boletin']
	 	pal_new   = []
	 	for y in tqdm(range(len(boletin)),"Obteniendo sinonimos de cada Proyecto"):
	 		id_proyecto =  boletin[str(y)]['id_proyecto']
	 		for pal in boletin[str(y)]['palabras']:
	 			pal_new.append(pal)
	 			try :
					sinonimos = get_Sinonimos(pal)
					for sin in sinonimos:
						pal_new.append(sin)
	 			except requests.exceptions.ConnectionError as err:
	 				log = open('log.txt','w')
	 				cad = "indice_sesion:"+str(i)+",indice_boletin:"+str(y)+",utlima_palabra:"+str(pal)
	 				log.write(cad)
	 				log.close()
	 				guardar(Json_sinonimos)
	 				print err
	 				sys.exit(1)
	 		Dic_Proyectos[y]={'id_proyecto':id_proyecto,'palabras':pal_new}
	 		pal_new = []
	 	Json_sinonimos[i] = {"id_sesion":id_sesion,"boletin":Dic_Proyectos}
	guardar(Json_sinonimos)

def continua_creacion(indice_sesion,indice_boletin,utlima_palabra):
	Json_sinonimos = {}
	with open('Palabras_Final.json') as f:
		Json_sinonimos = json.load(f)
	with open('Palabras.json','r') as f:
			 file = json.load(f)
			 continua_sesion = False
			 continua_boletin= False
			 continua_palabra = False
			 for i in tqdm(range(len(file)),"Progreso Total"):
				# Continua en el indice anterior , que quedo guardado en el log 
				#--------------------------------------------------------------
				if(i>int(indice_sesion)): continua_sesion = True
				if(continua_sesion):			 
				 	id_sesion = file[str(i)]['id_sesion']
				 	boletin   = file[str(i)]['boletin']
				 	pal_new   = []
				 	for y in tqdm(range(len(boletin)),"Obteniendo sinonimos de cada Proyecto"):
				 		# Continua en el indice anterior , que quedo guardado en el log 
				 		#--------------------------------------------------------------
				 		if(y > int(indice_boletin)): continua_boletin = True
				 		if(continua_boletin):	
					 		id_proyecto =  boletin[str(y)]['id_proyecto']
					 		for pal in boletin[str(y)]['palabras']:
					 			pal_new.append(pal)
					 			if(pal == utlima_palabra): continua_palabra=True
					 			if (continua_palabra == True):
						 			try :
										sinonimos = get_Sinonimos(pal)
										for sin in sinonimos:
											pal_new.append(sin)
						 			except requests.exceptions.ConnectionError as err:
						 				log = open('log.txt','w')
						 				cad = "indice_sesion:"+str(i)+",indice_boletin:"+str(y)+",utlima_palabra:"+str(pal)
						 				log.write(cad)
						 				log.close()
						 				guardar(Json_sinonimos)
						 				print err
						 				sys.exit(1)
					 		Dic_Proyectos[y]={'id_proyecto':id_proyecto,'palabras':pal_new}
					 		pal_new = []
				 	Json_sinonimos[i] = {"id_sesion":id_sesion,"boletin":Dic_Proyectos}
	guardar(Json_sinonimos)
#----------------------------------
#Conexion con mongodb 
#-----------------------------------

def Crear_Json():
	con = MongoClient("Localhost",27017)
	db  = con.parlamento
	#----------------------------------
	#Carga Coleccion 
	#----------------------------------
	quevotan = db.quevotan
	data = quevotan.find_one()
	sesiones = data['sesiones']

	Dic_palabras = {}
	dic_boletin  = {}	
	print "\n \n"
	for i in tqdm(range(len(data['sesiones'])),'Obteniendo Palabras '):
		boletin = sesiones[str(i)]['Boletin']
		for y in range(len(boletin)):
			#----------------------------------
			#Procesamiento de texto con NLTK --
			#----------------------------------
			detalle = boletin[str(y)]['detalle']
			palabras = nltk.word_tokenize(detalle)
			texto    = nltk.Text(palabras)
			corpu    = nltk.corpus.stopwords.words("spanish")
			tags     = nltk.pos_tag(palabras) #Obtiene tags con detalle de la palabra
			fdist = nltk.FreqDist(texto) #Busca palabras que mas se repitan en el texto
			a_tags =[]
			guardar = True
			#print tags
			
			#Quita palabras que contiene variable corpus
			for i2 in tags :
				if(i2[1] == 'NNP' and len(i2[0]) > 2):
					for y2 in range(len(corpu)) : 
						if ( i2[0].lower() == corpu[y2]):
							guardar = False
					if(guardar):
						a_tags.append(i2[0])
					guardar = True

			dic_boletin[y]={'id_proyecto':boletin[str(y)]['id'],'palabras':a_tags}
			#print boletin
		Dic_palabras[i] = {"id_sesion":sesiones[str(i)]['Id_sesion'],"boletin":dic_boletin}

	#-------------------------------------
	# Guarda json con palabras sin los sinonimos
	#---------------------------------------
	with open('Palabras.json', 'w') as file:
	    json.dump(Dic_palabras, file)

	print "Archivo Guardado  \n \n"
#Si el archivo no existe crea json
if ( os.path.isfile('Palabras.json') == False):
	Crear_Json()
else : 
	#Pregunta si el archivo esta vacio 
	with open('Palabras.json','r') as f:
		file = json.load(f)
		if (len(file) == 0 ):
			Crear_Json()
#-------------------------------------
# Cargar Json 
#---------------------------------------

Json_sinonimos = {}
Dic_Proyectos  = {}

#Continua con la creacion del json , carga de la ultima parte que quedo 
if( os.path.isfile('log.txt') == False ) : 
	Crear_Json()
else : 
	file = open('log.txt')
	cad  = file.read().split(',')
	indice_sesion = cad[0].split(':')[1]
	indice_boletin= cad[1].split(':')[1]
	utlima_palabra= cad[2].split(':')[1]
	if (indice_boletin == 'None' and indice_sesion == 'None' and utlima_palabra == 'None'):
		crear_json2()
	else:
		continua_creacion(indice_sesion,indice_boletin,utlima_palabra)



		








>>>>>>> Develop:lferreira/Obtener_Etiquetas(Anterior errores).py
