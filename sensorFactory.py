from EvFireSensor import EvFireSensor
from EvMotionSensor import EvMotionSensor
'''set cpu serial to true'''
def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial

'''create Motion Array of the sensors'''
def createMotionArray(motionSensorArray,isRasber):
    serial = "noserial"
    if isRasber == True:
        serial = getserial()
    s = EvMotionSensor(serial,5,5,'not in use',isRasber)     #turns neo on edge 9
    s.findMotionThread()
    motionSensorArray.append(s)
    s1 = EvMotionSensor(serial,6,7,'not in use',isRasber)    #turns neo on edge 11
    s1.findMotionThread()
    motionSensorArray.append(s1)
    s2 = EvMotionSensor(serial,16,11,'not in use',isRasber)  #turns neo on edge 19
    s2.findMotionThread()
    motionSensorArray.append(s2)
    s3 = EvMotionSensor(serial,13,9,'not in use',isRasber)#edge 14
    s3.findMotionThread()
    motionSensorArray.append(s3)
    s4 = EvMotionSensor(serial,23,13,'not in use',isRasber)#edge 17
    s4.findMotionThread()
    motionSensorArray.append(s4)
    s5 = EvMotionSensor(serial,20,15,'not in use',isRasber)#edge 27
    s5.findMotionThread()
    motionSensorArray.append(s5)

'''create fire sensor array of the sensors'''
def createFireSensorsArray(fireSensorArray,isRasber):
    serial = "noserial"
    if isRasber == True:
        serial = getserial()
    s = EvFireSensor(serial,27, 0, isRasber)
    if isRasber == True:
        from EvFireSensorRasbery import EvFireSensorRasbery
        s = EvFireSensorRasbery(serial,27, 0, isRasber)
    s.findFire()
    fireSensorArray.append(s)

    s1 = EvFireSensor(serial,4,2,isRasber)
    if isRasber == True:
       from EvFireSensorRasbery import EvFireSensorRasbery
       s1 = EvFireSensorRasbery(serial,4, 2, isRasber)
    s1.findFire()
    fireSensorArray.append(s1)
    
    s2 = EvFireSensor(serial,23,6,isRasber)
    if isRasber == True:
        from EvFireSensorRasbery import EvFireSensorRasbery
        s2 = EvFireSensorRasbery(serial,23,6,isRasber)
    s2.findFire()
    fireSensorArray.append(s2)
    
    s3 = EvFireSensor(serial,24,8,isRasber)
    if isRasber == True:
        from EvFireSensorRasbery import EvFireSensorRasbery
        s3 = EvFireSensorRasbery(serial,24,8,isRasber)
    s3.findFire()
    fireSensorArray.append(s3)
    
    s4 = EvFireSensor(serial,22,4,isRasber)
    if isRasber == True:
        from EvFireSensorRasbery import EvFireSensorRasbery
        s4 = EvFireSensorRasbery(serial,22,4,isRasber)
    s4.findFire()
    fireSensorArray.append(s4)
    
    s5 = EvFireSensor(serial,15,10,isRasber)
    if isRasber == True:
        from EvFireSensorRasbery import EvFireSensorRasbery
        s5 = EvFireSensorRasbery(serial,15,10,isRasber)
    s5.findFire()
    fireSensorArray.append(s5)
    
'''creates neo pixel array of the sensors'''
def createNeoPixelMap(isRasber):
    neoSensorMap = {}
    if (isRasber):
        from NeoPixelSensor import NeoPixelSensor
        import board
        import neopixel
        neoSensorMap = {
            27: NeoPixelSensor(board.D18,27),
            19: NeoPixelSensor(board.D12,19),
            11: NeoPixelSensor(board.D21,11),
            -1: NeoPixelSensor(board.D10,-1)
        }
    return neoSensorMap
           