#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo 
from nltk import * 
import time as t
import sys
import os
import json
from pymongo import MongoClient
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup



reload(sys)
sys.setdefaultencoding('utf8')

def get_Sinonimos(text):
	url = "http://www.wordreference.com/sinonimos/"+text
	resp = requests.get(url)
	sinonimos = []
	bs=BeautifulSoup(resp.text,'lxml')
	lista=bs.find_all(class_='trans clickable')
	for i in lista : 
		sin =  i.find_all('li')
	for i in sin : 
		if ( i.span == None ) : 
			for y in i.get_text().split(','):
				
				sinonimos.append(y.strip())
	return sinonimos

#print get_Sinonimos("RECONOCIMIENTO")

# #AT : Artículo
# #NN : Sustantivo
# #VB: Verbo
# #JJ: Adjetivo.
# #

#----------------------------------
#Conexion con mongodb 
#-----------------------------------
con = MongoClient("Localhost",27017)
db  = con.parlamento

# #----------------------------------
# #Carga Coleccion 
# #----------------------------------
quevotan = db.quevotan
data = quevotan.find_one()
sesiones = data['sesiones']

detalle  =  sesiones['0']['Boletin']['1']['detalle']


# #----------------------------------
# # Obtener etiquetas 
# #---------------------------------

corpu = corpus.stopwords.words("spanish")


token = word_tokenize(detalle)

tags  = pos_tag(token)

palabras = []
guardar = True


	

for i in tags :
	if(i[1] == 'NNP'):
		for y in range(len(corpu)) : 
			if ( i[0].lower() == corpu[y]):
				guardar = False
		if(guardar):
			palabras.append(i[0])
		guardar = True
#print tags

# #for i in tags : 
# #    if(i[1]=='NNP' and len(i[0])> 2): print i[0]
