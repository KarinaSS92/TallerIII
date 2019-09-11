import pymongo 
import nltk
import nltk.data
from pymongo import MongoClient



con = MongoClient("Localhost",27017)
db  = con.parlamento

#Coleccion 
quevotan = db.quevotan

data = quevotan.find_one()

sesiones = data['sesiones']
for i in range(len(data['sesiones'])):
	boletin = sesiones[str(i)]['Boletin']
	for y in range(len(boletin)):
		detalle = boletin[str(y)]['detalle']
		print detalle




