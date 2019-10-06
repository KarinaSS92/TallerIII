# ----- Carga de librerias ----- #
import json


#Apertura y carga del archivo original
with open('Palabras_Final.json') as file:
	file = json.load(file)
	#print file["0"]["boletin"]["0"]["palabras"]["2"]["sinonimos"]  #prueba de sintaxis
	final = {} #arreglo global que abarca todo el contenido

	# ----- Recorrido de toda las sesiones -----#
	for i in range(len(file)):
		aux = file[str(i)]

		if(len(aux["boletin"]) > 0): # existen boletines en la sesion?
			aux = aux["boletin"]
			boletin = {}  # diccionario de boletines
			# Recorrido de los boletines
			status = False
			for j in range(len(aux)):
				ref = aux[str(j)]

				if(len(ref["palabras"]) > 0): # existen palabras en el boletin?
					ref = ref["palabras"]
					palabras = {} # diccionario de palabras

					# Recorrido de las palabras
					for k in range(len(ref)):
						ref2 = ref[str(k)]

						if(len(ref2["sinonimos"]) > 0): # existen sinonimos
							palabras[k] = {'sinonimos':ref2["sinonimos"], 'cantidad': ref2["cantidad"], 'palabra': ref2["palabra"]}
							status = True
							
					boletin[j] = {'id_proyecto': aux[str(j)]["id_proyecto"],'palabras': palabras} # generacion del boletin
			if(status):
				final[i] = {'id_sesion':file[str(i)]["id_sesion"], "boletin":boletin}
	print final


# ----- Generacion de JSON Modificado ----- #
with open('new_palabras.json', 'w') as file:
	json.dump(final, file)