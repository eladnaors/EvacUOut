import neopixel
from datetime import datetime
import time

'''Neo Pixel Sensor - responsible for the flash showing
   here we show the flash sensor
'''
class NeoPixelSensor:
    def __init__(self,boardNum, edgeNum):
        
        self.pixel = neopixel.NeoPixel(boardNum, 55, brightness=1)
        self.pixel.fill((0, 0, 0))
        self.showNeoStarted = False
        self.showNeoStartX = -1
        self.edgeNum = edgeNum
        self.boardNum = boardNum
        self.index =1
        self.showNeoFinishX = 5
        if (self.edgeNum==-1):
            self.index=-1
            self.showNeoFinishX =-5
        
    def startFlash(self):
        print("Start flashing board " + str(self.edgeNum) + " " + str(self.boardNum))
        self.startTime = datetime.fromtimestamp(time.time())
        self.pixel.fill((0, 0, 0))
        self.showNeoStarted=True
        if (self.edgeNum != -1):
            self.showNeoStartsX=0
    
    def clear(self):
        self.pixel.fill((0, 0, 0))
    
    def flashspecial(self,n1,n2):
         self.showNeoFinishX=n2
         self.showNeoStartsX=n1
         
         self.flash()
            
    '''flash is worked as blink shows blink on the neo sensor
    from time to time.'''
    def flash(self):
        if (self.showNeoStarted==False):
            self.startFlash()
            
        deltaTime = datetime.fromtimestamp(time.time())
        delta = deltaTime - self.startTime
        difference = int(delta.total_seconds())

        if ((difference>self.showNeoFinishX and self.edgeNum!=-1) or (difference>self.showNeoFinishX and self.edgeNum==-1)):
            self.pixel.fill((0, 0, 0))
            self.showNeoStarted=False   
            return()
        
        difference = difference*self.index
        '''because neo sensor is going from top to bottom
        we set self.edgeNum as negative'''
        if (self.edgeNum==-1):
            self.pixel[11+self.showNeoStartsX+difference]=(255, 255, 0)
        else:
            self.pixel[difference]=(255, 255, 0)

 

            
                         