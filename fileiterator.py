import re
import os

file = open('index','w')
directory = input('Specified directory: ')
list = []
convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
lists = sorted(os.listdir(directory), key=alphanum_key)
list = lists
#file.write("#EXTINF:1.001,\n")
for filename in list:
#	file.write("\n")
	if filename.endswith(".mp4"):
		file.write("file \'"+directory+"/"+filename+"\'\n")
file.close
