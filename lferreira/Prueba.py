# Import libraries
import requests
import urllib
import time
from bs4 import BeautifulSoup

url = "http://opendata.camara.cl/wscamaradiputados.asmx/getSesionBoletinXML?prmSesionID=3737"
req = requests.get(url)
html = BeautifulSoup(req.text,"html.parser")

proyecto = html.find_all("proyecto_ley")
for script in  proyecto[0].find_all("intervencion_diputado"):
	script.decompose()

print proyecto[0].get_text()