from pygame import mixer
from mutagen.mp3 import MP3
from os import walk
import random
import time

class mp3Player:
    def __init__(self,folder):
        mixer.init()
        self.vol = 0.05
        self.folder = folder
        for (path, dirname, titles) in walk("//home//gmo//Music//"): #dir of music
                self.mixlist = titles
        self.currentSong = self.mixlist[0]
        
        
    def loadSong(self):
        
        mp3 = MP3(self.folder+"//"+self.currentSong) #dir of music
        freq = mp3.info.sample_rate
        mixer.quit() # you need to quite the mixer so the frequency can be properly set
        mixer.init(frequency=freq) #you need to set the frequence so that music playes correctly
        mixer.music.set_volume(self.vol)
        mixer.music.load(self.folder+"//"+self.currentSong) #dir of music
        
    def getRandom(self):
        random.shuffle(self.mixlist)
        if(self.mixlist[0] == self.currentSong):
            self.currentSong = self.mixlist[2]
        else:
            self.currentSong = self.mixlist[0]
            
    def Running(self):
        if(not mixer.music.get_busy()):
           print("1")
           self.nextSong()
           self.loadSong()
           mixer.music.play()
        
    def nextSong(self):
        print("3")
        currentIndex = self.mixlist.index(self.currentSong)
        if(self.mixlist[len(self.mixlist)-1] == self.currentSong):
            self.currentSong = self.mixlist[0]
        else:
            self.currentSong = self.mixlist[currentIndex+1]
            
    def prevSong(self):
        print("4")
        currentIndex = self.mixlist.index(self.currentSong)
        if(self.mixlist[0] == self.currentSong):
            self.currentSong = self.mixlist[len(self.mixlist)-1]
        else:
            self.currentSong = self.mixlist[currentIndex-1]
    def play(self):
        mixer.music.play()
    def unpause(self):
        mixer.music.unpause()
    def pause(self):
        mixer.music.pause()
    def stop(self):
        mixer.music.stop()
    def volPlus(self):
        self.vol += 0.01
        mixer.music.set_volume(self.vol)
    def volMinus(self):
        self.vol -= 0.01
        mixer.music.set_volume(self.vol)
