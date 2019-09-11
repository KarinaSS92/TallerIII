import pymongo 
import nltk
import nltk.data
import time as t
import sys
import json
from pymongo import MongoClient
from tqdm import tqdm

reload(sys)
sys.setdefaultencoding('utf8')

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
for i in range(len(data['sesiones'])):
	boletin = sesiones[str(i)]['Boletin']
	for y in range(len(boletin)):
		#----------------------------------
		#Procesamiento de texto con NLTK --
		#----------------------------------
		detalle = boletin[str(y)]['detalle']
		palabras = nltk.word_tokenize(detalle)
		texto    = nltk.Text(palabras)
		tags     = nltk.pos_tag(palabras) #Obtiene tags con detalle de la palabra
		fdist = nltk.FreqDist(texto) #Busca palabras que mas se repitan en el texto
		a_tags =[]
		for i2 in tags :
			if i2[1] =='NNP':
				a_tags.append(i2[0])


		dic_boletin[y]={'id_proyecto':boletin[str(y)]['id'],'palabras':a_tags}


		#print boletin
	Dic_palabras[i] = {"id_sesion":sesiones[str(i)]['Id_sesion'],"boletin":dic_boletin}


with open('Palabras.json', 'w') as file:
    json.dump(Dic_palabras, file)