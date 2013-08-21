import os, sys, subprocess

if ((len(sys.argv) != 2) or ((sys.argv[1] != "stop") and (sys.argv[1] != "start"))):
	print "Usage: python controlservers.py <arg>"
	print "\t arg = {stop, start}"
	sys.exit(1)

command = sys.argv[1]
print "%sing Nginx and Apache Servers..." % command

if command == "start":
	subprocess.call(["sudo", "service", "nginx"])
	subprocess.call(["sudo", "service", "apache2", "start"])

elif command == "stop":
	subprocess.call(["sudo", "nginx", "-s stop"])
	subprocess.call(["sudo", "service", "apache2", "stop"])

