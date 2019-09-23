import pymongo
import json


myclient = pymongo.MongoClient()
mydb = myclient["db-quevotan"]
mycol = mydb["colecciones"]


with open('datos.json') as file:
    data = json.load(file)

x = mycol.insert(data)
print "listo"
