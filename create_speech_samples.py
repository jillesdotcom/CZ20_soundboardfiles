# Author: Jilles Groenendijk
# 
# Purpose:
#   Create numbers and international spellings alphabeth
#
# Version:
# 1.00 - Initial release
#
import os,wifi,ugTTS

page=4
button=0

def create(text):
	global page,button
	newpath="/sd/soundboard/page"+str(page)
	if not os.path.isdir(newpath):
		os.mkdir(newpath)
	print(text)
	ugTTS.text_to_mp3(text,newpath+"/sound"+str(button)+".mp3")
	button=button+1
	if button>15:
		button=0
		page=page+1

wifi.connect()

if not wifi.wait():
	print("No wifi")
else:
	samples=["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", 
	"alfa", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "pappa", 
	"quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey", "xray", "yankee", "zulu"]
	samples="zero"
	for s in samples:
		create(s)

