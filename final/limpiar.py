from nltk import word_tokenize
from nltk.corpus import stopwords

import nltk
from pymongo import MongoClient


def connect():
	con = MongoClient("Localhost",27017)
	db  = con.parlamento
	quevotan = db.quevotan
	return quevotan.find_one()

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

f = open('pal_prueba.txt','w')
db = connect()
sesiones = db['sesiones']

for i in sesiones:
	boletin = sesiones[i]['Boletin']
	for y in boletin:
		detalle = boletin[y]['detalle']
		tokens = nltk.word_tokenize(detalle)
		tag = nltk.pos_tag(tokens)
		for x in tag :
			save = True
			if(x[1] == 'NNP' and len(x[0])>3):
				for j in x[0]:
					if(j == '.'):
						save = False
				for stop in stopwords.words('spanish'):
					if ( normalize(x[0].lower()) == normalize(stop) ) :
						save = False

				if(save):
					print (x[0].lower())
