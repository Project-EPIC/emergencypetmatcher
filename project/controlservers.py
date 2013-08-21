import os, sys, subprocess

if len(sys.argv) != 2 or sys.argv[1] not in ["stop", "start", "restart"]:
	print "Usage: python controlservers.py <arg>"
	print "\t arg = {stop, start, restart}"
	sys.exit(1)

command = sys.argv[1]
print "%sing Nginx and Apache Servers..." % command

#Execute process calls.
subprocess.call(["sudo", "service", "nginx", command])
subprocess.call(["sudo", "service", "apache2", command])
