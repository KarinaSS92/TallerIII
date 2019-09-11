# ----- Importacion de librerias ----- #
import re, string, unicodedata
import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk import FreqDist

# ----- Apertura y lectura de texto de pruba ----- #
archivo = open('texto.txt','r')
archivo = archivo.read().decode('utf8')

# ----- Procesamiento con BeautifulSoup ----- #
html = BeautifulSoup(archivo,'html.parser')
texto = html.get_text(strip=True);
#texto = re.sub('\[[^]]*\]', '', html)

# ----- Procesamiento de texto con NLTK ----- #
palabras = nltk.word_tokenize(texto)
texto = nltk.Text(palabras)

print texto.concordance("diputado") # Muestra el contexto en el que se encuentra la palabra
print texto.similar("pesca") # Reconoce palabras similares

comunes = FreqDist(texto)										# Obtiene la cantidad de veces que
print [i for i in comunes.most_common(1000) if len(i[0]) > 5]	# se repite cada palabra


