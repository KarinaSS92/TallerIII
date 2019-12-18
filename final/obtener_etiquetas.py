# -*- coding: utf-8 -*-
# Import libraries
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

#----------------------------------
#Funciones
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
	with open("json/Palabras_Final.json",'w') as f:
		json.dump(Dic,f)
def cargar_db():
	con = MongoClient("Localhost",27017)
	db  = con.parlamento
	quevotan = db.quevotan
	data = quevotan.find_one()
	sesiones = data['sesiones']
	return sesiones
def cargar_diputados():
	con = MongoClient("Localhost",27017)
	db  = con.parlamento
	diputados = db.diputados
	data = diputados.find_one()

	return data
def crea_log():
	file = open('log.txt','w')
	cad  = "indice_sesion:None,indice_boletin:None,utlima_palabra:None"
	file.write(cad)
	file.close()
def contar_veces(elemento,lista):
	veces = 0
	for i in lista:
		if elemento == i :
			veces +=1
<<<<<<< HEAD
	return veces
=======
	return veces 

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s
>>>>>>> Develop
#-----------------------------------------------------------
#Crea log y llama funcion donde ejecuta para crear sinonimos
#-----------------------------------------------------------
def archivo_palabras():
	crea_log()
	Crear_Json()
#-------------------------------------------------------------
#Crea json con palabras sin sinonimos , realiza parte de nltk
#------------------------------------------------------------
def Crear_Json():
	sesiones = cargar_db()
	diputados    = cargar_diputados()
	Dic_palabras = {}
	dic_boletin  = {}
	dic_cantidad ={}
	esNombre = False
	repite   = False
	print "\n \n"
	for i in tqdm(range(len(sesiones)),"Extrayendo Palabras"):
		boletin = sesiones[str(i)]['Boletin']
		for y in range(len(boletin)):
			#----------------------------------
			#Procesamiento de texto con NLTK --
			#----------------------------------
			cont = 0
			detalle = boletin[str(y)]['detalle']

			id_proyecto= boletin[str(y)]['id']
			palabras = nltk.word_tokenize(detalle)

			texto    = nltk.Text(palabras)
			words    = nltk.corpus.stopwords.words("spanish")
			tags     = nltk.pos_tag(palabras) #Obtiene tags con detalle de la palabra
			fdist    = nltk.FreqDist(texto) #Busca palabras que mas se repitan en el texto

			a_tags =[]
			guardar = True

			#Quita palabras que contiene variable words
			for i2 in tags :
<<<<<<< HEAD
				if(i2[1] == 'NNP' and len(i2[0]) > 2):
					for y2 in range(len(words)) :
						if ( i2[0].lower() == words[y2]):
=======
				if(i2[1] == 'NNP' and len(i2[0]) > 3):
					for ver in i2[0]:
						if(ver == '.'):
							guardar = False
					for y2 in range(len(words)) : 
						if ( normalize(i2[0].lower()) == normalize(words[y2])):
>>>>>>> Develop
							guardar = False
					if(guardar):
						esNombre= False
						#Busca si existe algun nombre , si es nombre no lo guarda
						for dipu in range(len(diputados)-1) :
							dipu = str(dipu)
							d_nombre = diputados[dipu]['nombre'].lower()
							d_ape_p  = diputados[dipu]['apellido_paterno'].lower()
							d_ape_m  = diputados[dipu]['apellido_materno'].lower()
							if(d_nombre == i2[0].lower() or d_ape_m == i2[0].lower() or d_ape_p == i2[0].lower() or 'senado' == i2[0].lower() or 'presidente' == i2[0].lower()):
								esNombre = True
						if(esNombre == False):
							a_tags.append(i2[0].lower())
					guardar = True
			#Busca las palabras que se repiten , si se repiten estas se guardan
			for x in a_tags:
				cantidad = contar_veces(x,a_tags)
				if(cantidad > 1):
					for cant in dic_cantidad:
						if (dic_cantidad[cant]['palabra'] == x): repite = True

					#Si la palabra ya se agrego , no se vuelve a guardar
					if ( repite == False):
						dic_cantidad[cont] = {'palabra':x,'cantidad':cantidad}
						cont +=1
				repite = False
			
			dic_boletin[y]={'id_proyecto':id_proyecto,'palabras':dic_cantidad}


			a_tags = []
			dic_cantidad={}
			#print boletin
		Dic_palabras[i] = {"id_sesion":sesiones[str(i)]['Id_sesion'],"boletin":dic_boletin}
		dic_boletin = {}
		cont=0


	#-------------------------------------
	# Guarda json con palabras sin los sinonimos
	#---------------------------------------
	with open('json/palabras.json', 'w') as file:
	    json.dump(Dic_palabras, file)

	print "Archivo Guardado  \n \n"

#-------------------------------------------------------------
#Crea Archivo que contiene los sinonimos , teniendo dos funciones uno que continua donde quedo
#-------------------------------------------------------------
def archivo_sinonimos():
	with open('json/palabras.json','r') as f:
	 Dic_Proyectos ={}
	 Json_sinonimos={}
	 dic_palabras  ={}
	 file = json.load(f)
	 for i in tqdm(range(len(file)),"Progreso Total"):
	 	id_sesion = file[str(i)]['id_sesion']
	 	boletin   = file[str(i)]['boletin']
	 	pal_new   = []
	 	for y in tqdm(range(len(boletin)),"Obteniendo sinonimos de cada Proyecto"):
	 		id_proyecto =  boletin[str(y)]['id_proyecto']
	 		palabras    = boletin[str(y)]['palabras']
	 		for pal in palabras:
	 			palabra = palabras[pal]['palabra']
	 			cantidad= palabras[pal]['cantidad']
	 			try :
					sinonimos = get_Sinonimos(palabra)
					dic_palabras[pal]={'palabra':palabra,'cantidad':cantidad,'sinonimos':sinonimos}
	 			except requests.exceptions.ConnectionError as err:
	 				log = open('log.txt','w')
	 				cad = "indice_sesion:"+str(i)+",indice_boletin:"+str(y)+",utlima_palabra:"+str(palabra)
	 				log.write(cad)
	 				log.close()
	 				guardar(Json_sinonimos)
	 				print err
	 				sys.exit(1)
	 		Dic_Proyectos[y]={'id_proyecto':id_proyecto,'palabras':dic_palabras}

	 		dic_palabras={}
	 	Json_sinonimos[i] = {"id_sesion":id_sesion,"boletin":Dic_Proyectos}
	 	Dic_Proyectos={}
	guardar(Json_sinonimos)
def archivo_sinonimos_Continuar(indice_sesion,indice_boletin,utlima_palabra):
	Dic_Proyectos ={}
 	Dic_sinonimos={}
 	dic_palabras  ={}
	with open('json/palabras.json','r') as f:
			 file = json.load(f)
			 continua_sesion = False
			 continua_boletin= False
			 continua_palabra = False
			 for i in tqdm(range(len(file)),"Progreso Total"):
				# Continua en el indice anterior , que quedo guardado en el log
				#--------------------------------------------------------------
				if(i>len(file)): continua_sesion = True
				if(continua_sesion):
				 	id_sesion = file[str(i)]['id_sesion']
				 	boletin   = file[str(i)]['boletin']
				 	pal_new   = []
				 	for y in tqdm(range(len(boletin)),"Obteniendo sinonimos de cada Proyecto"):
				 		# Continua en el indice anterior , que quedo guardado en el log
				 		#--------------------------------------------------------------
				 		if(y > len(boletin)): continua_boletin = True
				 		if(continua_boletin):
					 		id_proyecto =  boletin[str(y)]['id_proyecto']
					 		palabras    = boletin[str(y)]['palabras']
					 		for pal in palabras:
					 			palabra = palabras[pal]['palabra']
 								cantidad= palabras[pal]['cantidad']
					 			if(palabra == utlima_palabra): continua_palabra=True
					 			if (continua_palabra == True):
						 			try :
										sinonimos = get_Sinonimos(pal)
										dic_palabras[pal]={'palabra':palabra,'cantidad':cantidad,'sinonimos':sinonimos}
						 			except requests.exceptions.ConnectionError as err:
						 				log = open('log.txt','w')
						 				cad = "indice_sesion:"+str(i)+",indice_boletin:"+str(y)+",utlima_palabra:"+str(pal)
						 				log.write(cad)
						 				log.close()
						 				guardar(Dic_sinonimos)
						 				print err
						 				sys.exit(1)
					 		Dic_Proyectos[y]={'id_proyecto':id_proyecto,'palabras':pal_new}
					 		pal_new = []
				 	Dic_sinonimos[i] = {"id_sesion":id_sesion,"boletin":Dic_Proyectos}
				 	Dic_Proyectos={}
	guardar(Dic_sinonimos)


#---------------------------
#Variables Globales
#---------------------------
start= False
#------------------------------------
# Comprueba de que el archivo existe (Palabras.json)
#-------------------------------------
if ( os.path.isfile('json/palabras.json') == False):
	archivo_palabras()
else :
	#Pregunta si el archivo esta vacio
	with open('json/palabras.json','r') as f:
		file = json.load(f)
		if (len(file) == 0 ):
			archivo_palabras()
		else:
			start = True
#---------------------------------------
# Comprueba de que el archivo existe (log.txt)
#---------------------------------------
if ( start):
	if( os.path.isfile('log.txt') == False ) :
		print "Error No existe Log, Creando.."
		crea_log()
		archivo_sinonimos()
	else :
		if(os.path.isfile('json/Palabras_Final.json') == False):
			archivo_sinonimos()
		else:
			file = open('log.txt')
			cad  = file.read().split(',')
			indice_sesion = cad[0].split(':')[1]
			indice_boletin= cad[1].split(':')[1]
			utlima_palabra= cad[2].split(':')[1]
			if (indice_boletin == 'None' and indice_sesion == 'None' and utlima_palabra == 'None'):
				archivo_sinonimos()
			else:
				archivo_sinonimos_Continuar(indice_sesion,indice_boletin,utlima_palabra)
