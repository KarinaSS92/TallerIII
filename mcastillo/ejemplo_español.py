import sys
sys.stdout.encoding
'UTF-8'
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
example_sent = "RECONOCIMIENTO Y PROTECCI\u00d3N DE DERECHOS DE ENFERMOSTERMINALES A ATENCI\u00d3N ADECUADA Y MUERTE DIGNA(Primer tr\u00e1mite constitucional. Bolet\u00edn N\u00b0 12507-11)[Continuaci\u00f3n]El se\u00f1or FLORES, don Iv\u00e1n (Presidente).- En el Orden del D\u00eda, corresponde continuar la discusi\u00f3n del proyecto de ley, iniciado en mensaje, sobre reconocimiento y protecci\u00f3n de los derechos de las personas con enfermedades terminales, y el buen morir. "
hola=example_sent.encode('utf8')
print ("hola---------",hola)
stop_words = set(stopwords.words('spanish'))
word_tokens = word_tokenize(example_sent)
filtered_sentence = [w for w in word_tokens if not w in stop_words]
filtered_sentence = []
for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)
print("original---------",word_tokens)
print("filtrado---------",filtered_sentence)
