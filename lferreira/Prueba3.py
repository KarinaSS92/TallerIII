import requests
from bs4 import BeautifulSoup
import sys
try:
    r = requests.get('http://www.google.com/nothere')
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    file = open("log.txt","w")
    file.write("123")
    file.close()