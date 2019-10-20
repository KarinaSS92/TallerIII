#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

text = "Ministerio de Economía, Fomento y Turismo:Servicio Nacional de Pesca,SERNAPESCA,Servicio Nacional de Turismo,SERNATUR,Servicio Nacional del Consumidor,SERNAC,Instituto Nacional de Estadísticas de Chile,INE,Fiscalía Nacional Económica,FNE,Empresa de Abastecimiento de Zonas Aisladas,EMAZA,Sistema de Empresas Públicas,SEP,Corporación de Fomento de la Producción,CORFO,Servicio de Cooperación Técnica,SERCOTEC,Comité de Inversiones Extranjeras,CIE,pesca"
name = text.split(":")[0]
palabras = text.split(":")[1]
palabras = palabras.split(",")

json_test = {"Nombre": name, "palabras": palabras}

with open('prueba_busqueda.json', 'w') as file:
	json.dump(json_test, file)

