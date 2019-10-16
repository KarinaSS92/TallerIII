import json

file = open('Ministerios.txt','r')
Ministerios = {}
list_pal         = []
data = file.read().split(".")
for i in range(len(data)):
	mini =  data[i].split(":")[0]
	# Saca Salto de linea de Ministerios 
	salto = mini.split("\n")
	if(len(salto)> 0 ):
		for sal in salto:
			if ( len(sal) > 0 ):
				mini = sal
	data_2= data[i].split(":")
	for y in range(len(data_2)):
		if ( y != 0 ):
			palabras =  data_2[y].split(",")
			for pal in palabras :
				list_pal.append(pal.lower())
	Ministerios[i]={'Nombre':mini,'Palabras':list_pal}
	list_pal = []

with open('json/ministerios.json', 'w') as file:
    json.dump(Ministerios, file)