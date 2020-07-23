# Author: Jilles Groenendijk
# 
# Purpose:
#   Fix TTS glitch by creating dummy first and generate TTS audio later
#
# Version:
# 1.00 - Initial release
# 1.01 - added launcher
#
import os, system, wifi, ugTTS

wifi.connect()

if not wifi.wait():
	print("No wifi")
else:
	for appname in os.listdir("/apps"):
		filename="/cache/appnames/"+appname+".mp3"
		print("Checking filename: "+filename)
		if not(os.path.isfile(filename)):
			print("creating file: "+filename)
			fh = open(filename, "wb")
			fh.close
	for appname in os.listdir("/apps"):
		filename="/cache/appnames/"+appname+".mp3"
		print("Checking filename: "+filename)
		if os.path.isfile(filename):
			fh=open(filename, "rb")
			filesize=len(fh.read())
			fh.close()
			if(filesize==0):
				print("Dummy file:"+filename+" creating TTS")
				ugTTS.text_to_mp3(appname, filename)
system.launcher()
