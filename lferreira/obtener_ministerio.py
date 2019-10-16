file = open('Ministerios.txt','r')


Ministerios = []


for i in  file.read().split("."):
	Ministerios.append(i.split(":")[0])


print Ministerios