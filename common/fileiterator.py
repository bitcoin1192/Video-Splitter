import re
import os

def listfilebyformats(directory,format):
	file = open(directory+'index','w')
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	lists = sorted(os.listdir(directory), key=alphanum_key)
	for filename in lists:
		if filename.endswith("."+format):
			file.write("file \'"+directory+"/"+filename+"\'\n")
	file.close

