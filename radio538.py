import wifi, audio, time, system, sndmixer, display, keypad

if not wifi.status():
    audio.play('/cache/system/wifi_connecting.mp3')
    wifi.connect()
    wifi.wait()
    if not wifi.status():
        audio.play('/cache/system/wifi_failed.mp3')
        time.sleep(6)
        system.launcher()
    
time.sleep(3)
volume = 256
oldvolume = 256

def volumedraw(vol):
    vol1 = 0
    vol2 = 0
    vol3 = 0
    vol4 = 0
    if vol >= 63:
        vol1 = 255
        if vol >= 127:
            vol2 = 255
            if vol >= 192:
                vol3 = 255
                if vol >= 255:
                    vol4 = 255
                else:
                    vol4 = (volume - 192) * 4
            else:
                vol3 = (volume - 128) * 4
        else:
            vol2 = (volume - 64) * 4
    else:
        vol1 = (volume - 0) * 4
    display.drawPixel(0, 0, (vol1 << 16)+ (vol1 << 8) + vol1)
    display.drawPixel(1, 0, (vol2 << 16)+ (vol2 << 8) + vol2)
    display.drawPixel(2, 0, (vol3 << 16)+ (vol3 << 8) + vol3)
    display.drawPixel(3, 0, (vol4 << 16)+ (vol4 << 8) + vol4)
    display.flush()


def setvolume(vol):
    for index in audio.handles.keys():
        sndmixer.volume(index, vol)
    volumedraw(volume)  

def knopjes():
    display.drawPixel(0, 3, 0x008000)
    display.drawPixel(1, 3, 0x800000)
    display.drawPixel(2, 3, 0x800000)
    display.drawPixel(3, 3, 0x008000)
    display.flush()

  
def on_key(key_index, pressed):
    global volume, oldvolume
    x, y = key_index % 4, int(key_index / 4)
    if pressed:
        if y==3 and (x==1 or x==2):
            if volume > 0:
                oldvolume = volume
                volume = 0
            else:
                volume = oldvolume
        if y==3 and x==0:
            volume -= 64
        if y==3 and x==3:
            volume += 64
        if volume < 0:
            volume = 0
        if volume >= 256:
            volume = 255
        setvolume(volume)
url = 'http://21253.live.streamtheworld.com/RADIO538.mp3'
audio.play(url)
knopjes()
setvolume(volume)
keypad.add_handler(on_key)
