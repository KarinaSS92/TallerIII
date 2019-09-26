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





with open('json/palabras.json') as f :
	file = json.load(f)
	repeticion = {}
	boletin = file['0']['boletin']
	palabras = boletin['0']['palabras']
	print palabras
	a_pa = []
	for pal in palabras :

		cantidad = contar_veces(pal,palabras)
		val = (pal,cantidad)
		if(cantidad > 1 ):
			a_pa.append(val)
	