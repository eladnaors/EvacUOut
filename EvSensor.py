import graphCalculation
import time
from datetime import datetime
'''EVSensor - father class of all sensors
EvMotionSensor
EvFireSensor
EvFireSensorRasbery

This father class holds shared properties of the sensor'''
class EvSensor:
    _channel=-1
    _sensorType =""
    _sensorNumber = -1
    _sensorDirty = False
    _edgeNumber = -1
    _insideRasbery=False
    _rasberyNumber=""
    _timestamp=datetime.fromtimestamp(time.time())
    
    def __init__(self, sensorType,rasberyNumber, channel, sensorNumber,insideRasbery):
        self._rasberyNumber = rasberyNumber
        self._sensorType = sensorType
        self._channel = channel
        self._sensorNumber = sensorNumber
        self._insideRasbery = insideRasbery
    
    # using property decorator
    # a getter function
    @property
    def sensorTypeS(self):
         return self._sensorType
       
    # a setter function
    @sensorTypeS.setter
    def sensorTypeS(self, a):
         self._sensorType = a
         
    @property
    def timeStampS(self):
         return self._timestamp
       
    # a setter function
    @timeStampS.setter
    def timeStampS(self, a):
         self._timestamp = a     
         
    @property
    def channelS(self):
         return self._channel
       
    # a setter function
    @channelS.setter
    def channelS(self, a):
         self._channel = a
    
     # a getter function
    @property
    def sensorNumber(self):
         return self._sensorNumber
       
    # a setter function
    @sensorNumber.setter
    def sensorNumber(self, a):
         self._sensorNumber = a

    # a getter function
    @property
    def edgeNumber(self):
         return self._edgeNumber
       
    # a setter function
    @edgeNumber.setter
    def edgeNumber(self, a):
         self._edgeNumber = a

    @property
    def rasberyN(self):
         return self._rasberyNumber
    
    
    @property
    def sensorID(self):
         return self._rasberyNumber + "_"+ str(self._channel)
    # a setter function
    @rasberyN.setter
    def rasberyN(self, a):
         self._rasberyNumber = a

    # a getter function
    @property
    def sensorDirty(self):
         return self._sensorDirty
       
    # a setter function
    @sensorDirty.setter
    def sensorDirty(self, a):
         self._sensorDirty = a