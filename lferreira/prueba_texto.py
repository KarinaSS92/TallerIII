#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo 
from nltk import * 
import time as t
import sys
import json
from pymongo import MongoClient
from tqdm import tqdm



reload(sys)
sys.setdefaultencoding('utf8')


#AT : Artículo
#NN : Sustantivo
#VB: Verbo
#JJ: Adjetivo.
#

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

detalle  =  sesiones['0']['Boletin']['1']['detalle']


#----------------------------------
# Obtener etiquetas 
#---------------------------------

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
print tags
for i in tags :
	if i[1] == "CD":
		print i[0]
#for i in tags : 
#    if(i[1]=='NNP' and len(i[0])> 2): print i[0]
