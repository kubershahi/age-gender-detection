import os.path
from os import path

fread = open('prediction.txt', 'r')
fwrite = open('test_gender.txt',"w+")

female = 0 
male = 0

for line in fread:
	values = line.split()

	if (path.exists('Data/testgender/m/'+values[0])):
		data = values[0]+' '+values[1]+' 0'
		fwrite.write(data)
		male+=1
	elif(path.exists('Data/testgender/f/'+values[0])):
		data = values[0]+' '+values[1]+' 1'
		fwrite.write(data)
		female+=1

fread.close()
fwrite.close()

print(male)
print(female)	