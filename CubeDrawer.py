from twilio.rest import Client
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import sys
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation
from EvFireSensor import EvFireSensor
from EvMotionSensor import EvMotionSensor
from EvSensor import EvSensor
import dbFirebase
import sensorFactory 
import graphCalculation
import graphFactory
import igraph as ig
import time
from datetime import datetime
import threading
import json
import socket
global funcA
global fireSensorArray
global motionSensorArray
global mylock
global ax
global bx
global g
global db
global isRasber
global _isLoadingDb
global pause
global close_all
global screen_mode
global pixels1
global startTimes1
global showNeoStarts1
global showNeoStartsX
global _neoSensorMap
''' Global values used by all class '''
pause = False
close_all = []

'''Sensor and Motion arrays - we load it from DB and draw in on the screen'''
_fireSensorArray = []
_motionSensorArray = []

_isLoadingDb =[]
'''Lock used to synchronize between loading from DB and drawing.
When we load from DB we not draw'''
mylock = threading.Lock()
db = dbFirebase.firebaseDB()
'''Boolean isRasber holds if the computer used as sensor holder or for drawing
is isRasber true, it means code runs inside rasberypie and it connects to the 
sensors. but also it draws the result on the screen.
If isRasber is false it means we only draw the result'''
isRasber = "raspber" in socket.gethostname()
screen_mode="screen_mode"
print("isRasber",isRasber)
'''NeoSensorMap used to hold all neo lights sensors (only in rasbery)'''
_neoSensorMap = {}


'''First part used to UI operations on the screen'''
'''ON Click -> send whatsapp to fire apartment'''
def button1_clicked(event):
    account_sid = 'AC712010a428157abe8982a56a81c432b9'
    auth_token = '02eaee2ae94bae03c78e074014080425'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='FIRE!!! FIRE!!!',
        to='whatsapp:+972526224722',
    )
    print(message.sid)

'''On click change between Graph draw and Text draw only show evacuation vertex'''
def button2_clicked(event):
    global screen_mode
    if (screen_mode == "screen_mode"):
        print('canvas cleared')
        screen_mode = "text_mode"
    else:
        screen_mode = "screen_mode"
        ax.cla()
        drawSubplot()

''' ONCLICK the draw paused, and on other click the draw continues'''
def onClick(event):
    global pause
    pause = not pause
    if (pause==True):
        plt.title("Paused.Press click to continue ...", color="red", fontsize="20", fontweight="bold" ,y=-0.01, wrap=True)
    else:
        plt.title("Press click to pause ...", color="red", fontsize="20", fontweight="bold" ,y=-0.01, wrap=True)

''' ONCLOSE closes the form'''
def on_close(evt):
    print("closing...")
    for motionSensor in _motionSensorArray:
        motionSensor.stopFunction()
    close_all.append(1)

''' used to loadSensor from DB and add it to the sensors ARRAY
    We use _isLoadingDB array as lock -> 
    This thread and main thread holds the pointer to the array
    If we loads the sensors data, we put value inside it isLoadingDB array, 
    After we finish with loading, we clear isLoadingDB array '''
'''We load 3 arrays
_fireSensorArray - holds fire Sensor data
_motionSensorArray - holds motion Sensor data
if isRasber true, we create fireSensorArray 
'''
def loadSensors():
    global _fireSensorArray
    global _motionSensorArray
    global _isLoadingDB
    while len(close_all)==0:
        _isLoadingDb.append(1)
        print("thread 1 =>data received, starting", datetime.now())
        dbMotionDocs = db.collection(u'motionSensor').stream()
        _fireSensorArray.clear()
        _motionSensorArray.clear()
        for doc in dbMotionDocs:
            s = EvMotionSensor("",1,1,'----',False)
            s.fromjson = doc.to_dict()
            _motionSensorArray.append(s)
            
        dbFireDocs = db.collection(u'fireSensor').stream()
        for doc in dbFireDocs:
            s = EvFireSensor("noserial",1,1,False)
            if isRasber==True:
                from EvFireSensorRasbery import EvFireSensorRasbery
                s = EvFireSensorRasbery("noserial",1,1,False)
            s.fromjson = doc.to_dict()
            _fireSensorArray.append(s)
            

        print("thread 1 =>data received, waiting ", datetime.now())
        _isLoadingDb.clear()
        time.sleep(5)
            
'''The main draw function.
Returns ax graph object with all graph functionality and colors 
1 Draws fire Sensors 
2 Draws motion Sensors
3 Draws path.
If the computer is Rasbery, it also responsible for turn on the sensors on the
physical model:
1 Turn on fire lights (red lights)
2 Turn on motion Sensor (blue lights)
3 Turn on Neo Sen (Orange lights)'''
def drawSensors(self):
        global _fireSensorArray
        global _motionSensorArray
        global screen_mode
        global bx
        global pause
        global pixels1
        global startTimes1
        global showNeoStarts1
        global showNeoStartsX
        global _neoSensorMap
        if pause:
            return ax
        if len(_isLoadingDb)>0:
            return ax
        ''' create copy of arrays to use it for drawings'''
        fireSensorArray = _fireSensorArray.copy()
        motionSensorArray = _motionSensorArray.copy()
        resultsEdges=[]
        resultsVertexes = []
        hasFire = False
        hasMotion = False

        ''' if screen mode is text '''
        if (screen_mode == "text_mode"):
            ax.cla()
            ax.set_axis_off()
            for fireSensor in fireSensorArray:
                if (fireSensor.fireFound):
                    hasFire = True
                    break
            if (hasFire):
                resultsEdges,resultsVertexes = graphCalculation.calculateShortExitArrayNew(g, fireSensorArray, motionSensorArray)
                my_y=0.1
                my_x =0.1
                i=0
                res = ""
                '''Here we writes the path text on the screen'''
                for arrVertexes in resultsVertexes:
                    res = res +  "Path from the vertex number " + str(arrVertexes[0]) + " is :"
                    res = res + ','.join(str(f)  for f in arrVertexes) + "\n"
                ax.text(x=my_x, y=my_y, z=0.5, s=res,fontsize=20)

            else:
                ax.text(x=0.5, y=0.5, z=0.5, s="no fire",fontsize=20)
            '''We finish with the text and not continue with draw'''
            return ax

        for fireSensor in fireSensorArray:
            '''If there is fire, we draw fire sensor on the screen'''
            if (fireSensor.fireFound):
                hasFire = True
                currenttime= time.time()
                '''We also blink it '''
                fireSensor.change_blink_color()
                ax.get_lines()[fireSensor.edgeNumber].set_color(fireSensor.color)
                ax.get_lines()[fireSensor.edgeNumber].set_linewidth(fireSensor.lineWidth)


            elif (not fireSensor.fireFound):
                '''If there is not fire , shows the sensor black color'''
                ax.get_lines()[fireSensor.edgeNumber].set_color("black")
                ax.get_lines()[fireSensor.edgeNumber].set_linewidth(4)

        '''IF we found fire, we need to calculate short exit'''
        if (hasFire):
            resultsEdges,resultsVertexes  = graphCalculation.calculateShortExitArrayNew(g,fireSensorArray,motionSensorArray)
            print(resultsEdges)


        motionWithFlashArray=[]
        '''IF motion sensor array found '''
        for motionSensor in motionSensorArray:
            '''if motion found we add '''
            if (motionSensor.motionFound):
                hasMotion = True
                motionWithFlashArray.append(motionSensor.edgeNumber)
                #if (not results in resultsEdges):
                ax.get_lines()[motionSensor.edgeNumber].set_color("blue")
                ax.get_lines()[motionSensor.edgeNumber].set_linewidth(4)
            elif (not motionSensor.motionFound):
                ax.get_lines()[motionSensor.edgeNumber].set_color("black")
                ax.get_lines()[motionSensor.edgeNumber].set_linewidth(4)
        
        for i in range(0,len(ax.get_lines())):
            if (ax.get_lines()[i].get_color()=="#feb236" or ax.get_lines()[i].get_color()=="#3CB043" ):
                       ax.get_lines()[i].set_color("black")
        
            
        for neo in _neoSensorMap:
                _neoSensorMap[neo].clear()    
            
        if (hasFire and hasMotion):
            print(motionWithFlashArray)
            maxSensor = -1
            if (len(_neoSensorMap)>0):    
                for motionEdgeNumber in motionWithFlashArray:
                    if motionEdgeNumber in _neoSensorMap:
                        _neoSensorMap[motionEdgeNumber].flash()
                        if (maxSensor<motionEdgeNumber):
                            maxSensor=motionEdgeNumber

            if (maxSensor==27):
                    _neoSensorMap[-1].flashspecial(0,11)
            elif (maxSensor==19):
                    _neoSensorMap[-1].flashspecial(-5,11)
            elif (maxSensor==11):
                    _neoSensorMap[-1].flashspecial(-9,-11)
    
            for path in resultsEdges:
                    
                if (ax.get_lines()[path].get_color()=="#feb236" or ax.get_lines()[path].get_color()=="#3CB043"):
                    ax.get_lines()[path].set_color("#3CB043")
                else:
                    ax.get_lines()[path].set_color("#feb236")
                              
        return ax
'''drawSUBplot - draw the graph in the beginning
When the application is being start we calls the subplot draw'''
def drawSubplot():

    # Define the 8 vertices of the first cube
    vertices1 = np.array([(-0.25, 0, 0), (-0.25, 0.5, 0), (-0.25, 0.5, 1), (-0.25, 0, 1),
                          (0.25, 0, 0), (0.25, 0.5, 0), (0.25, 0.5, 1), (0.25, 0, 1)])

    # Define the 12 edges of the first cube by specifying pairs of vertices
    edges1 = [(0, 1), (1, 2), (2, 3), (3, 0),
              (0, 4), (1, 5), (2, 6), (3, 7),
              (4, 5), (5, 6), (6, 7), (7, 4)]

    # Define the 8 vertices of the second cube, which is placed directly above the first cube
    vertices2 = vertices1 + np.array([0.5, 0, 0])

    # Define the 12 edges of the second cube by specifying pairs of vertices
    edges2 = [(i+4, j+4) for (i, j) in edges1]

    # Define the 8 vertices of the third cube, which is placed directly above the second cube
    vertices3 = vertices2 + np.array([0.5, 0, 0])
    # Define the 12 edges of the third cube by specifying pairs of vertices
    edges3 = [(i+8, j+8) for (i, j) in edges1]

    # Combine the vertices and edges of all three cubes into a single array
    vertices = np.concatenate([vertices1, vertices3])
    edges = edges1 + edges2[4:8] + edges3
    print("edges=",edges)
    # Plot the vertices as blue dots, with labels
    for i, vertex in enumerate(vertices):
        ax.scatter(vertex[2], vertex[1], vertex[0], color='blue')
        ax.text(vertex[2], vertex[1], vertex[0], f'({i})', color='blue')

    index=0
    for edge in edges:
        ax.plot([vertices[edge[0],2], vertices[edge[1],2]],
                [vertices[edge[0],1], vertices[edge[1],1]],
                [vertices[edge[0],0], vertices[edge[1],0]], "black", linewidth=4)

    # Set the limits of the plot so that all three cubes are centered
    ax.set_xlim([-0.5, 0.9])
    ax.set_ylim([0, 0.7])
    ax.set_zlim([-0.5, 0.9])

    '''Removing the axis plots'''
    ax.set_axis_off()
    '''Draws the model with all existed colors to show legend'''
    ax.get_lines()[0].set_color("red")
    ax.get_lines()[0].set_label("fire")
    ax.get_lines()[1].set_color("blue")
    ax.get_lines()[1].set_label("motion")
    ax.get_lines()[2].set_color("orange")
    ax.get_lines()[2].set_label("path")
    ax.get_lines()[3].set_color("#3CB043")
    ax.get_lines()[3].set_label("multiple paths")

    '''Shows legend '''
    legend = ax.legend()
    legend.bbox_to_anchor = (0, 0)

    # Put a nicer background color on the legend.
    legend.get_frame().set_facecolor('C0')
    '''Removes all red, blue and orange colors'''
    ax.get_lines()[0].set_color("black")
    ax.get_lines()[1].set_color("black")
    ax.get_lines()[2].set_color("black")
    plt.title("Press click to pause ...", color="red", fontsize="20", fontweight="bold", y=-0.01, wrap=True)

'''Adds different cube events'''
def prepareCube():
    global ax
    global bx
    # Show the plot

    # Create a figure and add a 3D subplot
    fig = plt.figure(figsize=(10, 10))

    fig.canvas.mpl_connect('key_press_event', onClick)

    # Connect the `onclose` event to the figure
    fig.canvas.mpl_connect('close_event', on_close)

    # Create button widgets
    button1_ax = plt.axes([0.02, 0.75, 0.2, 0.05])
    button1 = Button(button1_ax, 'Call Fire Dept')
    button1.on_clicked(button1_clicked)

    button2_ax = plt.axes([0.02, 0.55, 0.2, 0.05])
    button2 = Button(button2_ax, 'View evacuation paths')
    button2.on_clicked(button2_clicked)
    # Adjust the spacing between the plot and the buttons
    plt.subplots_adjust(left=0.2, bottom=0.1, right=0.9, top=0.9)

    ax = fig.add_subplot(111, projection='3d')

    drawSubplot()
    plt.ion()
    plt.show()

    '''If sensor is Rasber we save it to the DB'''
    if (isRasber):
        dbFirebase.savemotionSensors(db,_motionSensorArray)
        dbFirebase.savefireSensors(db,_fireSensorArray)
    plt.draw()
    '''Start the thread of loading Sensors'''
    s2 = threading.Thread(target=loadSensors, args=())
    s2.start()
    '''Start the animation process 
    Animation process calls every 200 millisecond drawSensor function'''
    funcA = FuncAnimation(plt.gcf(), drawSensors, interval=200, repeat=True)
    
    input("Press [enter] to continue.")

    '''Start all loop loads sensor, prepare Cube, create motion and fire
    sensor'''
_name_='_main_'
if _name_ == '_main_':
    g = ig.Graph()
    graphFactory.buildplotgraph(g)
    dbFirebase.clearDB(isRasber)
    sensorFactory.createMotionArray(_motionSensorArray,isRasber)
    sensorFactory.createFireSensorsArray(_fireSensorArray,isRasber)
    _neoSensorMap = sensorFactory.createNeoPixelMap(isRasber)
    prepareCube()

