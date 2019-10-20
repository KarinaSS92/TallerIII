#!/usr/bin/env python
# -*- coding: utf-8 -*-

from difflib import SequenceMatcher as SM
import json

# ----- Funcion almacena ["Nombre ministerio", [arreglo de palabras encontradas por boletin], contador de puntos] ----- #
def reset():
	array = [["Ministerio del Interior y Seguridad Publica",[],0],
		 ["Ministerio de Relaciones Exteriores",[],0],
		 ["Ministerio de Defensa Nacional",[],0],
		 ["Ministerio Secretaria General de Gobierno",[],0],
		 ["Ministerio de Hacienda",[],0],
		 ["Ministerio de Economia, Fomento y Turismo",[],0],
		 ["Ministerio de Educacion",[],0],
		 ["Ministerio de Justicia y Derechos Humanos",[],0],
		 ["Ministerio del Trabajo y Prevision Social",[],0],
		 ["Ministerio de Obras Publicas",[],0],
		 ["Ministerio de Salud",[],0],
		 ["Ministerio de Vivienda y Urbanismo",[],0],
		 ["Ministerio de Agricultura",[],0],
		 ["Ministerio de Mineria",[],0],
		 ["Ministerio de Transportes y Telecomunicaciones",[],0],
		 ["Ministerio de Bienes Nacionales",[],0],
		 ["Ministerio de Energia",[],0],
		 ["Ministerio del Medio Ambiente",[],0],
		 ["Ministerio del Deporte",[],0],
		 ["Ministerio de la Mujer y la Equidad de Genero",[],0],
		 ["Ministerio de las Culturas, las Artes y el Patrimonio",[],0],
		 ["Ministerio de Ciencia, Tecnologia, Conocimiento e Innovacion",[],0]
		]
	return array

# ----- Inicio ----- #
dic_busqueda = open('ministerios.json')
file = open('new_palabras.json')
busqueda = json.load(dic_busqueda)
texto = json.load(file)
radio = 0.65 # punto de % de similitud minima para considerar la palabra como perteneciente a un ministerio

# ----- Recorre las sesiones ----- #
for i in texto:
	puntero = texto[str(i)]
	boletin = puntero["boletin"]
	id_sesion = puntero["id_sesion"] # LVL 1

	# ----- Recorre los boletines ----- #
	for j in boletin:
		boletin_actual = boletin[str(j)]
		palabra = boletin_actual["palabras"]
		ministerios = reset()

		# ----- Recorre las palabras ----- #
		for k in palabra:
			palabra_actual = palabra[str(k)]["palabra"]
			cantidad = palabra[str(k)]["cantidad"]
			
			# ----- Recorre el json Ministerios ----- #
			for l in busqueda:
				nombre_ministerio = busqueda[str(l)]["Nombre"]
				palabras_ministerio = busqueda[str(l)]["Palabras"]

				# ----- Recorre las palabras del ministerio actual ----- #
				for m in range(len(palabras_ministerio)):
					# Compara el % de similitud con la palabra analizada del boletin(palabra_actual)
					if SM(None, palabras_ministerio[m], palabra_actual).ratio() >= radio:
						# Recorre los ministerios hasta encontrar a cual pertence la palabra
						for n in range(len(ministerios)):
							if nombre_ministerio == ministerios[n][0]:
								bandera = True
								for o in range(len(ministerios[n][1])): # Revisa que la palabra se repite en ese ministerio
									if palabra_actual == ministerios[n][1][o]:
										bandera = False
								if bandera == True: # si no se repite la guarda y suma su cantidad al contador
									ministerios[n][1].append(palabra_actual)
									ministerios[n][2] = ministerios[n][2]+cantidad
		mayor = ministerios[0][2]
		name = ministerios[0][0]
		# Determina que ministerio tiene mayor numero de coincidencias con el texto
		for i in range(len(ministerios)):
			if mayor < ministerios[i][2]:
				mayor = ministerios[i][2]
				name = ministerios[i][0]
			if mayor == ministerios[2]:
				mayor = "hay dos"   # (Provisoria, Necesita cambio) cambiar para solucion multiple
		print boletin_actual["id_proyecto"], "==>", name