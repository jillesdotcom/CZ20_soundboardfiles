# 1.00 - Initial version by Renze Nicolai
# 1.01 - Added option to select 16 pages, allowing 256 samples
# 1.02 - Fixed error sample didn't work after switching to non existing one
# 1.03 - Fixed page 15 error, added cancel to go to page 1.
# 1.04 - Files now in dirs
# 1.05 - Adhere to volume settings + boot animation

#	Usage:
#		Play sample while holding the button (up to 4 at once)
#
#	Requires:
#		MP3 Samples on the SD Card
#
#	Button:
#		Play sample 
#
#	Touchpad:
#		Ok	 - Show current page
#		Cancel - Go to Page 1
#		Left   - Previous page
#		Right  - Next page
#
#	Sample files:
#		/soundboard/page<page nr>/sound0.mp3 -  sound15.mp3
#
#	Conversion via FFMPEG:
#		ffmpeg -i original.mp3 -ar 22050 -ac 1  -b:a 128k soundboardfile.mp3
#
#import system, os, display, keypad, touchpads, machine, sndmixer, virtualtimers as vt, random
import system, os, time, machine, appconfig, os, display, keypad, touchpads, sndmixer

settings = appconfig.get("soundboard", {"SampleFolder": "/sd/soundboard"})
print("Samplefolder:",settings['SampleFolder'])

MAX_FILES	= 4
MAX_PAGES	= 16

sndmixer.begin(MAX_FILES, False)

global_playing		= [False]*MAX_FILES
global_file			= [None]*MAX_FILES
global_channels		= [None]*MAX_FILES
global_filenames	= [""]*MAX_FILES
global_page			= 0

def load_file(filename):
	global global_playing, global_file, global_channels, global_filenames, MAX_FILES

	filepath = settings["SampleFolder"]+"/page"+str(global_page)+"/"+filename

	try:
		if filename in os.listdir(settings["SampleFolder"]+"/page"+str(global_page)):
			for i in range(MAX_FILES):
				if global_filenames[i] == filepath:
					print("File already open",filepath,"in slot",i)
					return i
			for i in range(MAX_FILES):
				if not global_playing[i]:
					if global_file[i]:
						global_file[i].close()
					global_file[i] = open(filepath, "rb")
					global_filenames[i] = filepath
					print("Opened file",filepath,"in slot",i)
					return i
		else:
			print(filepath,"does not exist")
			return None
	except:
		print("Failed to open",filepath)
		return None
		
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
		volume = machine.nvs_getint("system", "volume") or 255
		print("Volume:",volume)
		sndmixer.volume(channel, volume)
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
	
	print("Key",key_index,"on page",global_page,"pressed" if pressed else "released")

	filename = "sound{}.mp3".format(key_index)
	index = load_file(filename)

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

	if pressed==0:
		draw(global_page,False)
	else:
		if pressed == touchpads.CANCEL:
			global_page=0
		if pressed == touchpads.LEFT:
			if global_page>0:
				global_page=global_page-1
			else:
				global_page=(MAX_PAGES-1)

		if pressed == touchpads.RIGHT:
			if global_page<(MAX_PAGES-1):
				global_page=global_page+1
			else:
				global_page=0

		draw(global_page,True)
	print("new page",global_page)

touchpads.on(touchpads.OK, on_touch)
touchpads.on(touchpads.LEFT, on_touch)
touchpads.on(touchpads.RIGHT, on_touch)
touchpads.on(touchpads.CANCEL, on_touch)

keypad.add_handler(on_key)

for p in range(0,16):
	nofilesfound=True
	for b in range(0,16):
		filename=settings["SampleFolder"]+"/page"+str(p)+"/sound"+str(b)+".mp3"
		if os.path.isfile(filename):
			nofilesfound=False
	draw(p,True,nofilesfound)

for i in range(0,16):
	time.sleep(0.1)
	draw(15-i,False)
