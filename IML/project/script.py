import shutil, os

file = open('fold_frontal_0_data.txt', 'r')

male = 0 
female = 0
for line in file:
	values = line.split()
	img = 'faces/' + values[0] +'/'+ 'coarse_tilt_aligned_face.' + values[2] + '.' + values[1]

	if values[4] == "f":
		female+=1
		shutil.copy(img, 'Data/Gender/f')
	elif values[4] == "m":
		male+=1
		shutil.copy(img, 'Data/Gender/m')

print(male)
print(female)