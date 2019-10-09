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


reload(sys)
sys.setdefaultencoding('utf-8')


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




class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(538, 429)
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(110, 20, 191, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 20, 59, 15))
        self.label.setObjectName("label")
        self.pushButton =QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(320, 20, 80, 23))
        self.pushButton.setObjectName("pushButton")


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.buscar_palabra)



    def buscar_palabra(self):
        con = MongoClient("Localhost",27017)
        db  = con.parlamento

        #Cargar db 
        quevotan = db.quevotan
        palabras = db.palabras

        data_votan = quevotan.find_one()
        data_pal = palabras.find_one()
        sesiones = data_votan['sesiones']


        pal_buscar = self.lineEdit.text()
        texto = "No existe"

        id_list = []



        if (pal_buscar == " "): 
            QMessageBox.warning(Dialog, 'Error', "Campo Vacio !! ")
        else : 
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
                            else:
                                sinonimos = palabras[pal]['sinonimos']
                                for sin in sinonimos:
                                    if (normalize(sin) == normalize(pal_buscar)):
                                        texto = "existe"
        if ( texto == 'No existe'):
            QMessageBox.warning(Dialog, 'Error', "Palabra no encontrada en base de datos")


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Buscador"))
        self.label.setText(_translate("Dialog", "Buscar:"))
        self.pushButton.setText(_translate("Dialog", "Enviar"))








          
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

