#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----- Importacion de librerias ----- #
import re, string, unicodedata, codecs
import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize, wordpunct_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer, SnowballStemmer

# ----- Apertura y lectura de texto de pruba ----- #
def archivo():
	archivo = codecs.open('texto.txt', 'r')
	archivo = archivo.read()
	return pros_bs4(archivo)

# ----- Procesamiento con BeautifulSoup ----- #
def pros_bs4(dato):
	html = BeautifulSoup(dato)
	print html.original_encoding # Devuelve la coficacion del texto procesado con beautifulsoup
	texto = html.get_text()
	return pros_nltk(texto)

# ----- Procesamiento de texto con NLTK ----- #
def pros_nltk(info):
	lista = nltk.word_tokenize(info) # Genera lista de palabras
	texto = nltk.Text(lista)
	excluciones = set(stopwords.words('spanish')) # Genera lista de conectores en español
	filtrado = [i for i in texto if not i in excluciones and i not in "proyectos"] # elimina de la lista o arreglo los conectores
	#print filtrado # Devuelve el arreglo excluyendo conextores
	etiquetas = nltk.pos_tag(filtrado) #genera etiquetas para identificar a que tipo de palabra pertenece cada elemento de la lista
	#print etiquetas

	verbos = [i for i in etiquetas if(i[1] == 'VB' or i[1] == 'VBD' 
								or i[1] == 'VBG' or i[1] == 'VBN' 
								or i[1] == 'VBP' or i[1] == 'VBZ')]
	# ^ Obtiene los verbos encontrados en la lista ^
	#print verbos

	sustantivos = [i for i in etiquetas if(i[1] == 'NNS' or i[1] == 'NN' 
										or i[1] == 'NNP' or i[1] == 'NNPS')]
	# ^ Obtiene sustantivos encontrados en la lista ^
	#print sustantivos

	auxiliar = [] # Engloba los sustantivos y verbos en un solo arreglo
	for i in range(len(verbos)):
		auxiliar.append(verbos[i][0])
	for j in range(len(sustantivos)):
		auxiliar.append(sustantivos[j][0])
	#print auxiliar

	#print texto.concordance("diputado") # Muestra el contexto en el que se encuentra la palabra
	#print texto.similar("pesca") # Reconoce palabras similares

	comunes = FreqDist(auxiliar)										# Obtiene la cantidad de veces que
	#print [i for i in comunes.most_common(1000) if len(i[0]) > 5]	# se repite cada palabra
	clave = comunes.most_common(1)
	clave = clave[0]
	return clave[0]

palabra = archivo()
print palabra