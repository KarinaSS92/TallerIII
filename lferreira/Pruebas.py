from PyQt5.QtWidgets import *
import sys
from pymongo import MongoClient

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)

        # auto complete options 
        con = MongoClient("Localhost",27017)
        db  = con.parlamento 
        palabras = db.palabras.find_one()

        list_pal = []
        for i in palabras :
        	if (i != '_id'):
        		bol = palabras[i]['boletin']
        		for y in bol : 
        			pal = bol[y]['palabras']
        			for x in pal:
        				pass
        				#list_pal.append(pal[x]['palabra']) 
        				for sin in pal[x]['sinonimos']:
        					pass
        					#list_pal.append(sin) 
        file = open("Ministerios.txt","r")
        data = file.read().split(".")
        for i in range(len(data)):
        	mini =  data[i].split(":")[0]
        	salto = mini.split("\n")
        	if(len(salto)> 0 ):
        		for sal in salto:
        			if ( len(sal) > 0 ):
        				list_pal.append(sal.lower())
        	data_2= data[i].split(":")
        	for y in range(len(data_2)):
        		if ( y != 0 ):
        			palabras =  data_2[y].split(",")
        			for pal in palabras :
        				pass
        				#list_pal.append(pal.lower())
        list_pal = list(set(list_pal))

        print (list_pal)
        completer = QCompleter(list_pal)

        # create line edit and add auto complete                                
        self.lineedit = QLineEdit()
        self.lineedit.setCompleter(completer)
        layout.addWidget(self.lineedit, 0, 0)

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())