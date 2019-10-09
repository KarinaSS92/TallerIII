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



def contar_veces(elemento,lista):
	veces = 0
	for i in lista:
		if elemento == i :
			veces +=1
	return veces 

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
	with open("json/Palabras_Final_prueba.json",'w') as f:
		json.dump(Dic,f)


with open('json/palabras.json','r') as f:
 Dic_Proyectos ={}
 Json_sinonimos={}
 dic_palabras  ={}
 file = json.load(f)
 for i in tqdm(range(file),"Progreso Total"):
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


 	Dic_Proyectos ={}
 	Dic_sinonimos={}
 	dic_palabras  ={}

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
	guardar(Json_sinonimos)