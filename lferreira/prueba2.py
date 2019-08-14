import requests
import urllib
import time
import base64
from bs4 import BeautifulSoup


url = "https://www.camara.cl/img.aspx?prmid=chs1008"

imagen = requests.get(url).content
file = open("foto2.jpg", 'wb')
with file as handler:
	handler.write(imagen)
file.close()