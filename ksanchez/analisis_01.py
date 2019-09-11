#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
import nltk.data

# texto="La iniciativa tiene por objeto corregir algunos problemas derivados de
# implementación de la ley que creó el Sistema de Desarrollo Profesional Docente
# y otros cuerpos legales. En ese sentido, se pretende apoyar la implementación
# del referido sistema, mejorando el ingreso de los docentes directivos; propone
# un mecanismo que permita apoyar de mejor manera a los establecimientos
# educacionales con desempeño insuficiente; la prestación del servicio
# educacional en escuelas cárceles, o dependientes del Servicio Nacional de
# Menores y aulas hospitalarias, y mejora diversos aspectos del funcionamiento y
# las facultades de los administradores provisionales de establecimientos
# educacionales, entre otras materias."
texto="La iniciativa tiene por objeto corregir algunos problemas derivados de implementación de la ley que creó el Sistema de Desarrollo Profesional Docente y otros cuerpos legales. En ese sentido, se pretende apoyar la implementación del referido sistema, mejorando el ingreso de los docentes directivos; propone un mecanismo que permita apoyar de mejor manera a los establecimientos educacionales con desempeño insuficiente; la prestación del servicio educacional en escuelas cárceles, o dependientes del Servicio Nacional de Menores y aulas hospitalarias, y mejora diversos aspectos del funcionamiento y las facultades de los administradores provisionales de establecimientos educacionales, entre otras materias."
tokens= nltk.word_tokenize(texto)

#print tokens
tags=nltk.pos_tag(tokens)
print tags
i=0
for i in tags:
    if i[1]=='FW':
        print i
