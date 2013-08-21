import os, sys, urllib, urllib2

MINIFY_URL_JS = "http://javascript-minifier.com/raw"
MINIFY_URL_CSS = "http://cssminifier.com/raw"

if len(sys.argv) != 2:
	print "Usage: python minify.py <JS/CSS file>"
	sys.exit(1)

inputfile = sys.argv[1]
f = open(inputfile, "r")

#Grab the file format (.js or .css)
print "Readying the POST request for minification..."
input_filename = inputfile.split("/")[-1]
input_fileformat = input_filename.split(".")[-1]
input_name = input_filename.split(".")[0]

#Package the javascript in this dictionary.
args = {"input": f.read()}
data = urllib.urlencode(args)

if input_fileformat == "js":	
	request = urllib2.Request(MINIFY_URL_JS, data)

elif input_fileformat == "css":
	request = urllib2.Request(MINIFY_URL_CSS, data)

else:
	print "[ERROR]: Incorrect file format."
	sys.exit(1)

#Get the response back!
response = urllib2.urlopen(request)
minified = response.read()

#Now package it into a file.
new_file_name = input_name + ".min." + input_fileformat
print "Minifying %s into %s..." % (input_filename, new_file_name)
new_file = open(new_file_name, "w")
new_file.write(minified)
new_file.close()

#Remember to close the file.
response.close()
print "[OK]: Done. Minified file is in current directory."