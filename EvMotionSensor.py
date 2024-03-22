import graphCalculation
from EvSensor import EvSensor
from gpiozero import MotionSensor
#import RPi.GPIO as GPIO
from datetime import datetime
import time
import threading
import dbFirebase
db = dbFirebase.firebaseDB()


class EvMotionSensor(EvSensor):
    
    _motionFound = False
    _checkMotion = False
    _secondVertex = -1
    _color = ""
    close_all = []
    '''inits motion sensor'''
    def __init__(self,rasberyNumber, channel,sensorNumber,color,insideRasbery):
        EvSensor.__init__(self,"motion", rasberyNumber,channel,sensorNumber,insideRasbery)
        sensor1 = sensorNumber
        sensor2 = sensorNumber + 1
        if (sensor2 % 4==0):
            sensor2 = sensor1 - 3
        self._secondVertex = sensor2     
        self.edgeNumber = graphCalculation.getedgefrom2vertex(sensor1,sensor2)
        self._color = color
        self._checkMotion = True
    
    def stopFunction(self):
        self.close_all.append(1)
        
    def save2db(self):
        if (self._insideRasbery):
            db.collection(u'motionSensor').document(str(self.sensorID)).set(self.tojson)    

    '''find motion thread 
    check if the motion found inside rasbery pie'''
    def findMotionThread(self):
        if self._insideRasbery:
            t = threading.Thread(target=self.findMotion, args=())
            t.start()
            print("started")

    '''find motion connects to the motion sensor by some channel
    it always checks if there is some motion
    it waits on "pir.wait_for_motion" untill there will be some motion
    if it founds motion, it calls function whenMotion'''
    def findMotion(self):
        pir = MotionSensor(self._channel)
        while len(self.close_all)==0:
            
            if self._checkMotion:
                self.whenNoMotion()
                '''pir.wait_for_motion = blocking synchronized function'''
                pir.wait_for_motion()
                self.whenMotion()

            time.sleep(15)
        
    @property
    def motionFound(self):
         return self._motionFound
       
    # a setter function
    @motionFound.setter
    def motionFound(self, a):
         self._motionFound = a
         
    @property
    def checkMotion(self):
         return self._checkMotion
       
    # a setter function
    @checkMotion.setter
    def checkMotion(self, a):
         self._checkMotion = a
                
    @property
    def callOnMotionS(self):
         return self.callOnMotion
       
    # a setter function
    @callOnMotionS.setter
    def callOnMotionS(self, a):
         self.callOnMotion = a
         
    def whenMotion(self):
        self._motionFound = True
        print("motion found for sensor with edge=", self._edgeNumber)
        self.save2db()
        #self.callOnMotionS()
    def whenNoMotion(self):
        self._motionFound = False
        print("no motion found for sensor with edge=", self._edgeNumber)
        self.save2db()
        
    @property
    def idx1Graph(self):
        return self._sensorNumber
    
    @property
    def idx2Graph(self):
        return self._secondVertex
    
    @property
    def color(self):
        return self._color

    @property
    def motionMessage(self):
        return str(self.idx1Graph) + "--" + str(self.idx2Graph) + " (edge " + str(self.edgeNumber)  + ")"
    ''' Function tojson and fromjson used to convert object 
        to string json format and from string json format'''

    @property
    def tojson(self):
        
        tojson = {
            u'rasberyId' : self.sensorID,
            u'rasberyNumber' : str(self._rasberyNumber),            
            u'channel' : str(self._channel),
            u'sensorNumber': str(self._sensorNumber),
            u'color': str(self._color),
            u'sensorType': str(self._sensorType),
            u'motionFound': str(self._motionFound),
            u'sensorDirty': str(self._sensorDirty),
            u'checkMotion': str(self._checkMotion),
            u'edgeNumber':  str(self.edgeNumber),
            u'timeStamp':str(self._timestamp)
        }
        
        
        return tojson
    
    @tojson.setter
    def fromjson(self,json):
        #print("myjson=",json)
        self._channel = int(json['channel'])
        self._rasberyNumber = json['rasberyNumber']
        self._sensorNumber = int(json['sensorNumber'])
        self._secondVertex = self.sensorNumber + 1
        if (self._secondVertex % 4==0):
            self._secondVertex = self._sensorNumber - 3
        self._color = json['color']
        self._sensorType = json['sensorType']
        self._motionFound = (json['motionFound']=="True")
        self._checkMotion = (json['checkMotion']=="True")
        self._sensorDirty = (json['sensorDirty']=="True")
        self.edgeNumber = int(json['edgeNumber'])
        self._timestamp= datetime.strptime(json['timeStamp'],'%Y-%m-%d %H:%M:%S.%f')
        
        
    