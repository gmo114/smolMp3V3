from player import mp3Player
import RPi.GPIO as GPIO
import sys
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7789


# setting up  gpio pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(13,GPIO.OUT)
#end of setup

#display start
disp = ST7789.ST7789(
        height=240,
        width=240,
        rotation=90,
        port=0,
        cs=1,
        dc=9,
        backlight=None,
        spi_speed_hz=60 * 1000 * 1000,
        offset_left=0,
        offset_top=0
   )
#sets up back light
bw = GPIO.PWM(13,500)
bw.start(100)
#end of back light
# rest of setup
disp.begin()
WIDTH = disp.width
HEIGHT = disp.height
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
#end of display set up 

def write(message):
    draw.rectangle((0, 0, 240, 240), (0, 0, 0))
    draw.text((int(0),0), message, font=font, fill=(255, 255, 255))
    disp.display(img)
    
def fixmessage(message):
    max = 0
    newlist = []
    temp = ""
    for a in message:
        if(max == 22):
            newlist.append(temp)
            temp = ""
            max = 0
        max += 1
        temp += a
    newlist.append(temp)
    return newlist
    
    
def update(message,script):
    start = 0
    for a in fixmessage(message):
        script.append(a)      
    if(len(script) > 6):
        print(len(script))
        start = len(script)-6
        
    finalScript = ""
    for a in script:
        finalScript = finalScript+a+"\n"
    write(finalScript)
    return script[start:]

if __name__ == "__main__":
    script = []
    time2 = time.time
    
    script = update("click A to start music player",script)
    
    while(GPIO.input(5)):
        time.sleep(0.1)
        
    player = mp3Player("//home//gmo//Music//")
    player.stop()
    player = mp3Player("//home//gmo//Music//")
    player.loadSong()
    player.play()
    script = update("currently playing: "+player.currentSong,script)
    stop = False
    pause = False
    tm = 0.0
    br = 100
    while not stop:
        if(tm > 3 and br > 0.0):
            br -= 2
        bw.ChangeDutyCycle(br)
        answer  = [not GPIO.input(5),not GPIO.input(6),not GPIO.input(16),not GPIO.input(24)]
        #checks if the a new song is playing if so it will update the dipslay
        # this was need because Running will not update the display when the a new song get loaded
        currentSongCheck = player.currentSong
        player.Running()
        if currentSongCheck != player.currentSong:
            script[len(script)-1]="------------------------------------"
            script = update("currently playing: "+player.currentSong,script)
            bw.ChangeDutyCycle(100) #this is the only exception as to how I change the brightness in for loop
            br = 100
        #end of check
        
        if answer == [True,False,False,False]:# pause/play
            if(not pause):
                player.pause()
                pause = True
            else:
                player.unpause()
                pause = False
            time.sleep(0.15)
            br = 100
            tm = 0.0
        elif answer == [True,True,True,True]:# stop
            stop = True
            player.stop()
            write("you have stop the mp3 player")
            time.sleep(5)
            write("good bye!")
            time.sleep(1.5)
            bw.ChangeDutyCycle(0.0)
        elif answer == [False,False,True,False]: # vol plus
            player.volPlus()
            br = 100
            tm = 0.0
        elif answer == [False,False,False,True]: # vol minus
            player.volMinus()
            br = 100
            tm = 0.0
        elif answer == [False,True,False,True]: # Get Random playlist
            player.getRandom()
            player.loadSong()
            player.play()
            script[len(script)-1]="------------------------------------"
            script = update("currently playing: "+player.currentSong,script)
            br = 100
            tm = 0.0
        elif answer == [False,False,True,True]:
            player.nextSong()
            player.loadSong()
            player.play()
            script[len(script)-1]="------------------------------------"
            script = update("currently playing: "+player.currentSong,script)
            br = 100
            tm = 0.0
        elif answer == [True,True,False,False]:
            player.prevSong()
            player.loadSong()
            player.play()
            script[len(script)-1]="------------------------------------"
            script = update("currently playing: "+player.currentSong,script)
            br = 100
            tm = 0.0
            
        elif answer == [True,False,True,False]:
            script = update("A+B = stop",script)
            script = update("X = vol up",script)
            script = update("Y = vol down",script)
            script = update("B+Y = get next rand song",script)
            time.sleep(2)
            br = 100
            tm = 0.0
        tm += 0.15
        time.sleep(0.15)
