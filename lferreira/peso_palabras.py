# Import libraries
import nltk
import nltk.data
import sys
import json
from tqdm import tqdm
import matplotlib as mpl
#import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf8')

palabras = []
file     = {}
with open('Palabras.json') as f :
	file = json.load(f)	

for i in range (len(file)):
	boletin = file[str(i)]['boletin']
	for y in range(len(boletin)):
		aPalabras =  boletin[str(y)]['palabras']
		for pal in aPalabras : 
			palabras.append(pal)


freq = nltk.FreqDist(palabras)
freq.plot(20, cumulative=False)
for key,val in freq.items():
 	print (str(key) + ':' + str(val))