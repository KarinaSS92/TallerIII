import pymongo 
import nltk
import nltk.data
import time as t
import sys
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
#----------------------------------
#Conexion con mongodb 
#-----------------------------------
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
for i in tqdm(range(len(data['sesiones']))):
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
					if i2[0] == None: print "True"
					sinonimos = get_Sinonimos(i2[0])
					for sin in sinonimos :
						a_tags.append(sin)
				guardar = True


		dic_boletin[y]={'id_proyecto':boletin[str(y)]['id'],'palabras':a_tags}


		#print boletin
	Dic_palabras[i] = {"id_sesion":sesiones[str(i)]['Id_sesion'],"boletin":dic_boletin}


with open('Palabras.json', 'w') as file:
    json.dump(Dic_palabras, file)