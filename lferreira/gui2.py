# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from pymongo import MongoClient
from tqdm import tqdm
import sys
import time as t

reload(sys)
sys.setdefaultencoding('utf-8')


def contar_veces(elemento,lista):
    veces = 0
    for i in lista:
        if elemento == i :
            veces +=1
    return veces 

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

def Palabras_ministerios() :
    file = open("Ministerios.txt","r")
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
    return Ministerios



def obtener_nombre_dipu(id_d):
    con = MongoClient("Localhost",27017)
    db  = con.parlamento

    diputados= db.diputados.find_one()
    
    for i in diputados:
        if(i != "_id"):
            id_diputado = str(diputados[i]['id_diputado'])
            if(id_diputado == id_d):
                return [id_diputado,diputados[i]['nombre'],diputados[i]['apellido_paterno']]
               
class Ui_vtn(object):





    def setupUi(self, vtn):
        vtn.setObjectName("vtn")
        vtn.resize(800, 429)
        vtn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        
        self.txt_buscar = QLineEdit(vtn)
        self.txt_buscar.setGeometry(QtCore.QRect(110, 20, 191, 21))
        self.txt_buscar.setObjectName("txt_buscar")
        
        self.lbl_buscar = QLabel(vtn)
        self.lbl_buscar.setGeometry(QtCore.QRect(50, 20, 59, 15))
        self.lbl_buscar.setObjectName("lbl_buscar")
        
        self.enviar = QPushButton(vtn)
        self.enviar.setGeometry(QtCore.QRect(320, 20, 80, 23))
        self.enviar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.enviar.setObjectName("enviar")

        self.label_2 = QLabel(vtn)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 91, 16))
        self.label_2.setObjectName("label_2")

        self.list_id = QComboBox(vtn)
        self.list_id.setGeometry(QtCore.QRect(120, 80, 79, 23))
        self.list_id.setObjectName("list_id")
        self.text_detalle =QPlainTextEdit(vtn)
        self.text_detalle.setGeometry(QtCore.QRect(30, 170, 311, 241))
        self.text_detalle.setFrameShape(QFrame.Box)
        self.text_detalle.setObjectName("text_detalle")

        self.lbl_detalle = QLabel(vtn)
        self.lbl_detalle.setGeometry(QtCore.QRect(30, 140, 131, 16))
        self.lbl_detalle.setObjectName("lbl_detalle")

        self.lbl_votaciones = QLabel(vtn)
        self.lbl_votaciones.setGeometry(QtCore.QRect(400, 80, 151, 16))
        self.lbl_votaciones.setObjectName("lbl_votaciones")

        self.tabla_votaciones = QTableWidget(vtn)
        self.tabla_votaciones.setGeometry(QtCore.QRect(390, 110, 400, 301))
        self.tabla_votaciones.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tabla_votaciones.setFrameShape(QFrame.Box)
        self.tabla_votaciones.setFrameShadow(QFrame.Raised)
        self.tabla_votaciones.setObjectName("tabla_votaciones")

        self.tabla_votaciones.setRowCount(200)
        self.tabla_votaciones.setColumnCount(3)
        self.tabla_votaciones.setHorizontalHeaderLabels(('id_Diputado', 'Nombre','Apellido')) 

        self.list_votaciones = QComboBox(vtn)
        self.list_votaciones.setGeometry(QtCore.QRect(500, 80, 79, 23))
        self.list_votaciones.setObjectName("list_votaciones")

        self.line = QFrame(vtn)
        self.line.setGeometry(QtCore.QRect(50, 50, 351, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(vtn)
        QtCore.QMetaObject.connectSlotsByName(vtn)
        vtn.setTabOrder(self.txt_buscar, self.list_id)
        vtn.setTabOrder(self.list_id, self.text_detalle)
        vtn.setTabOrder(self.text_detalle, self.tabla_votaciones)
        vtn.setTabOrder(self.tabla_votaciones, self.list_votaciones)
        vtn.setTabOrder(self.list_votaciones, self.enviar)

        self.enviar.clicked.connect(self.buscar_palabra)
        self.list_id.currentTextChanged.connect(self.cambiar_proyecto)
        self.list_votaciones.currentTextChanged.connect(self.cambiar_votaciones)

        list_vota = ['Positivas','Negativas','Abstencion']
        self.id_list = []

        self.list_votaciones.addItems(list_vota)

    def retranslateUi(self, vtn):
        _translate = QtCore.QCoreApplication.translate
        vtn.setWindowTitle(_translate("vtn", "Buscador"))
        self.lbl_buscar.setText(_translate("vtn", "Buscar:"))
        self.enviar.setText(_translate("vtn", "Enviar"))
        self.label_2.setText(_translate("vtn", "Id_proyectos :"))
        self.lbl_detalle.setText(_translate("vtn", "Detalle de Proyecto : "))
        self.lbl_votaciones.setText(_translate("vtn", "Votaciones : "))
   
    def buscar_palabra(self):


        texto = "No existe"
        self.Ministerios = Palabras_ministerios()
        self.list_id.clear()
        self.text_detalle.clear()
        self.tabla_votaciones.clear()
        self.tabla_votaciones.setHorizontalHeaderLabels(('id_Diputado', 'Nombre','Apellido')) 
        con = MongoClient("Localhost",27017)
        db  = con.parlamento

        #Cargar db 
        quevotan = db.quevotan
        palabras = db.palabras

        data_votan = quevotan.find_one()
        data_pal = palabras.find_one()
        sesiones = data_votan['sesiones']
        guardar = True

        pal_buscar = self.txt_buscar.text()
        palabra_separada = pal_buscar.split(" ")
        if(len(pal_buscar.split(" ")) > 1 ):
            for i in range(len(self.Ministerios)):
                mini= normalize(self.Ministerios[i]['Nombre'].strip().lower()) 
                if (mini == pal_buscar.lower()):
                    pal =  self.Ministerios[i]['Palabras']
                    for x in pal : 
                        x =  x.strip()
                        #Busca palabras relacionadas con el ministerio
                        for i in data_pal:
                            if ( i != '_id'):
                                boletin = data_pal[i]['boletin']
                                for bol in boletin : 
                                    id_proyecto = boletin[bol]['id_proyecto']
                                    palabras    = boletin[bol]['palabras']
                                    for pal in palabras : 
                                        palabra =  palabras[pal]['palabra']
                                        if (normalize(palabra) == normalize(x)):
                                            texto = "existe"
                                            if (contar_veces(self.id_list,id_proyecto) <= 1):
                                                self.id_list.append(id_proyecto)

                                        else:
                                            sinonimos = palabras[pal]['sinonimos']
                                            for sin in sinonimos:
                                                if (normalize(sin) == normalize(x)):
                                                    texto = "existe"
                                                    if( contar_veces(self.id_list,id_proyecto) <= 1):
                                                        self.id_list.append(id_proyecto)

                        if(len(self.id_list) > 0 ):

                            for x in range (self.list_id.count()):
                                if (self.list_id.itemText(x) != None):
                                    item = self.list_id.itemText(x)

                                    for in_list in self.id_list:
                                        if (in_list == item):
                                            guardar = False

                            if ( guardar) :
                                self.list_id.addItems(self.id_list)
                                list_positivas = []
                                primer_id = self.id_list[0]

                                for i in range(len(sesiones)):
                                    boletin=sesiones[str(i)]['Boletin']
                                    for y in boletin : 
                                        id_p = boletin[y]['id']
                                        if (id_p == primer_id):
                                            self.text_detalle.insertPlainText(boletin[y]['detalle'])
                                            list_positivas.append(boletin[y]['votaciones']['votos']['si'])

                                for i in range(len(list_positivas[0])):
                                    id_d = list_positivas[0][i]
                                    datos_d = obtener_nombre_dipu(id_d)
                                    if ( datos_d != None):
                                        for y in range(len(datos_d)):
                                            if (datos_d[y] != " "):
                                                self.tabla_votaciones.setItem(i,y, QTableWidgetItem(datos_d[y]))



            if ( texto == 'No existe'):
                QMessageBox.warning(vtn, 'Error', "Palabra no encontrada en base de datos")

            pal = []

        else : 
            self.id_list = []

            continuar = False

            if (pal_buscar == ""): 
                QMessageBox.warning(vtn, 'Error', "Campo Vacio !! ")
            else : 
                continuar = True
            if ( continuar):
                for i in data_pal:
                    if ( i != '_id'):
                        boletin = data_pal[i]['boletin']
                        for bol in boletin : 
                            id_proyecto = boletin[bol]['id_proyecto']
                            palabras    = boletin[bol]['palabras']
                            for pal in palabras : 
                                palabra =  palabras[pal]['palabra']
                                if (normalize(palabra) == normalize(pal_buscar)):
                                    texto = "existe"
                                    if( contar_veces(self.id_list,id_proyecto) <= 1):
                                        self.id_list.append(id_proyecto)
                                else:
                                    sinonimos = palabras[pal]['sinonimos']
                                    for sin in sinonimos:
                                        if (normalize(sin) == normalize(pal_buscar)):
                                            texto = "existe"
                                            if( contar_veces(self.id_list,id_proyecto) <= 1):
                                                self.id_list.append(id_proyecto)

                if(len(self.id_list) > 0 ):
                    for x in range (self.list_id.count()):
                        if (self.list_id.itemText(x) != None):
                            item = self.list_id.itemText(x)
                            for in_list in self.id_list:
                                if (in_list == item):
                                    guardar = False


                    if(guardar):
                        self.list_id.addItems(self.id_list)
                        list_positivas = []
                        primer_id = self.id_list[0]

                        for i in range(len(sesiones)):
                            boletin=sesiones[str(i)]['Boletin']
                            for y in boletin : 
                                id_p = boletin[y]['id']
                                if (id_p == primer_id):
                                    self.text_detalle.insertPlainText(boletin[y]['detalle'])
                                    list_positivas.append(boletin[y]['votaciones']['votos']['si'])

                        for i in range(len(list_positivas[0])):
                            id_d = list_positivas[0][i]
                            datos_d = obtener_nombre_dipu(id_d)
                            if ( datos_d != None):
                                for y in range(len(datos_d)):
                                    if (datos_d[y] != " "):
                                        self.tabla_votaciones.setItem(i,y, QTableWidgetItem(datos_d[y]))


            if ( texto == 'No existe'):
                QMessageBox.warning(vtn, 'Error', "Palabra no encontrada en base de datos")

    def cambiar_proyecto(self):

    
        self.text_detalle.clear()
        self.tabla_votaciones.clear()
        self.tabla_votaciones.setHorizontalHeaderLabels(('id_Diputado', 'Nombre','Apellido')) 

        indice = self.list_id.currentIndex()
        id_proyecto =  self.id_list[indice]

        con = MongoClient("Localhost",27017)
        db  = con.parlamento

        #Cargar db 
        quevotan = db.quevotan
        palabras = db.palabras

        data_votan = quevotan.find_one()
        sesiones = data_votan['sesiones']

        list_positivas =[]
        for i in range(len(sesiones)):
            boletin=sesiones[str(i)]['Boletin']
            for y in boletin : 
                id_p = boletin[y]['id']
                if (id_p == id_proyecto):
                    self.text_detalle.insertPlainText(boletin[y]['detalle'])
                    list_positivas.append(boletin[y]['votaciones']['votos']['si'])

        for i in range(len(list_positivas[0])):
            id_d = list_positivas[0][i]
            datos_d = obtener_nombre_dipu(id_d)
            if ( datos_d != None):
                for y in range(len(datos_d)):
                    if (datos_d[y] != " "):
                        self.tabla_votaciones.setItem(i,y, QTableWidgetItem(datos_d[y]))
   

    def cambiar_votaciones(self):

        self.tabla_votaciones.clear()
        self.tabla_votaciones.setHorizontalHeaderLabels(('id_Diputado', 'Nombre','Apellido')) 

        indice = self.list_id.currentIndex()

        if(len(self.id_list) > 0 ) :
            id_proyecto =  self.id_list[indice]

            indice_votacion = self.list_votaciones.currentIndex()


            con = MongoClient("Localhost",27017)
            db  = con.parlamento

            #Cargar db 
            quevotan = db.quevotan
            palabras = db.palabras

            data_votan = quevotan.find_one()
            sesiones = data_votan['sesiones']

            list_vota =[]
            for i in range(len(sesiones)):
                boletin=sesiones[str(i)]['Boletin']
                for y in boletin : 
                    id_p = boletin[y]['id']
                    if (id_p == id_proyecto):
                        if (indice_votacion == 0):
                            list_vota.append(boletin[y]['votaciones']['votos']['si'])
                        if  (indice_votacion == 1):
                            list_vota.append(boletin[y]['votaciones']['votos']['no'])
                        if  (indice_votacion == 2):
                            list_vota.append(boletin[y]['votaciones']['votos']['abstencion'])
            
            for i in range(len(list_vota[0])):
                id_d = list_vota[0][i]
                datos_d = obtener_nombre_dipu(id_d)
                if ( datos_d != None):
                    for y in range(len(datos_d)):
                        if (datos_d[y] != " "):
                            self.tabla_votaciones.setItem(i,y, QTableWidgetItem(datos_d[y]))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    vtn = QDialog()
    ui = Ui_vtn()
    ui.setupUi(vtn)
    vtn.show()
    sys.exit(app.exec_())

