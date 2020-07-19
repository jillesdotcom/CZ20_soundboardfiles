# Initial author: Renze Nicolai
# Added multiple pages by: Jilles Groenendijk

import system, display, keypad, touchpads, machine, sndmixer, virtualtimers as vt, random

MAX_FILES = 4
MAX_PAGES = 16
sndmixer.begin(MAX_FILES)

global_playing   = [False]*MAX_FILES
global_file      = [None]*MAX_FILES
global_channels  = [None]*MAX_FILES
global_filenames = [""]*MAX_FILES
global_page      = 0

def load_file(filename):
	global global_playing, global_file, global_channels, global_filenames, MAX_FILES
	try:
		for i in range(MAX_FILES):
			if global_filenames[i] == filename:
				print("File already open",filename,"in slot",i)
				return i
		for i in range(MAX_FILES):
			if not global_playing[i]:
				if global_file[i]:
					global_file[i].close()
				global_file[i] = open(filename, "rb")
				global_filenames[i] = filename
				print("Opened file",filename,"in slot",i)
				return i
	except:
		print("Failed to open",filename)
	return None

def draw(button, active, error=False):
	x = button %  4
	y = button // 4
	color = 0xFFFFFF
	if error:
		color = 0xFF0000
	display.drawPixel(x, y, color if active else 0x000000)
	display.flush()

def play(index):
	global global_playing, global_file, global_channels, global_filenames, MAX_FILES
	if index < 0 or index > MAX_FILES:
		print("Play: invalid index")
	if global_playing[index]:
		print("Play: already playing")
		return
	channel = sndmixer.mp3_stream(global_file[index])
	if not channel:
		print("Play: invalid channel id")
		return
	try:
		sndmixer.play(channel)
	except:
		pass
	global_channels[index] = channel
	global_playing[index] = True

def stop(index):
	global global_playing, global_file, global_channels, global_filenames, MAX_FILES
	if index < 0 or index > MAX_FILES:
		print("Stop: invalid index")
	if not global_playing[index]:
		print("Stop: not playing")
		return
	channel = global_channels[index]
	if not channel:
		print("Stop: invalid channel id")
		return
	fd = global_file[index]
	if not fd:
		print("Stop: invalid fd")
		return
	try:
		sndmixer.stop(channel)
	except:
		pass
	global_playing[index] = False
	fd.seek(0)

def on_key(key_index, pressed):
	global global_page

	print("Key",key_index,"on page ",global_page,"pressed" if pressed else "released")
	index = load_file("/sd/sound{}.mp3".format((MAX_PAGES*global_page)+key_index))
	print("/sd/sound{}.mp3".format((MAX_PAGES*global_page)+key_index),index)
	if index != None:
		draw(key_index, pressed, False)
		if pressed:
			play(index)
		else:
			stop(index)
	else:
		draw(key_index, pressed, True)

def on_touch(pressed):
	global global_page
	
	if pressed == touchpads.LEFT:
		if global_page>0:
			global_page=global_page-1
		else:
			global_page=MAX_PAGES

	if pressed == touchpads.RIGHT:
		if global_page<MAX_PAGES:
			global_page=global_page+1
		else:
			global_page=0
	draw(global_page,True)
	draw(global_page,False)

touchpads.on(touchpads.LEFT, on_touch)
touchpads.on(touchpads.RIGHT, on_touch)

keypad.add_handler(on_key)
