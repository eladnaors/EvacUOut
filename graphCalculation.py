'''this function returns edge number from 2 given vertex'''
def getedgefrom2vertex(first, second):
    num=-999
    if (first==0 and second ==1) or (first==1 and second ==0) :
        num = 0
    if (first==1 and second ==2) or (first==2 and second ==1) :
        num = 1
    if (first==2 and second ==3) or (first==3 and second ==2) :
        num = 2
    if (first==3 and second ==0) or (first==0 and second ==3) :
        num = 3
    if (first==0 and second ==4) or (first==4 and second ==0) :
        num = 4
    if (first==1 and second ==5) or (first==5 and second ==1) :
        num = 5
    if (first==2 and second ==6) or (first==6 and second ==2) :
        num = 6
    if (first==3 and second ==7) or (first==7 and second ==3) :
        num = 7
    if (first==4 and second ==5) or (first==5 and second ==4) :
        num = 8
    if (first==5 and second ==6) or (first==6 and second ==5) :
        num = 9
    if (first==6 and second ==7) or (first==7 and second ==6) :
        num = 10
    if (first==4 and second ==7) or (first==7 and second ==4) :
        num = 11
    if (first==4 and second ==8) or (first==8 and second ==4) :
        num = 12
    if (first==5 and second ==9) or (first==9 and second ==5) :
        num = 13
    if (first==6 and second ==10) or (first==10 and second ==6) :
        num = 14
    if (first==7 and second ==11) or (first==11 and second ==7) :
        num = 15
    if (first==8 and second ==9) or (first==9 and second ==8) :
        num = 16
    if (first==9 and second ==10) or (first==10 and second ==9) :
        num = 17
    if (first==10 and second ==11) or (first==11 and second ==10) :
        num = 18
    if (first==11 and second ==8) or (first==8 and second ==11) :
        num = 19
    if (first==8 and second ==12) or (first==12 and second ==8) :
        num = 20
    if (first==9 and second ==13) or (first==13 and second ==9) :
        num = 21
    if (first==10 and second ==14) or (first==14 and second ==10) :
        num = 22
    if (first==11 and second ==15) or (first==15 and second ==11) :
        num = 23
    if (first==12 and second ==13) or (first==13 and second ==12) :
        num = 24
    if (first==13 and second ==14) or (first==14 and second ==13) :
        num = 25
    if (first==14 and second ==15) or (first==15 and second ==14) :
        num = 26
    if (first==15 and second ==12) or (first==12 and second ==15) :
        num = 27
    return num
    
    '''get graphshotest path handler - calculates shortes path
    to the nearest exit
    uses plot option to find the shortest path betweem 2 graphs'''
def getgraphshortespathandlen(g):
    source = g.vs.find(Motion=True)
    minlen=999
    minarray=[]
    '''here we use weight option 
    if in the edge there is a fire
    it means this edge is '''
    resultsswo = g.get_all_shortest_paths(source, to='SW0', weights=g.es["weight"], mode='out')
    for arr in resultsswo:
        if len(arr)<minlen:
            minlen=len(arr)
            minarray=arr
    resultsnwo = g.get_all_shortest_paths(source, to='NW0', weights=g.es["weight"], mode='out')
    for arr in resultsnwo:
        if len(arr)<minlen:
            minlen=len(arr)
            minarray=arr

    resultsseo = g.get_all_shortest_paths(source, to='SE0', weights=g.es["weight"], mode='out')
    for arr in resultsseo:
        if len(arr)<minlen:
            minlen=len(arr)
            minarray=arr
    resultsneo = g.get_all_shortest_paths(source, to='NE0', weights=g.es["weight"], mode='out')
    for arr in resultsneo:
        if len(arr)<minlen:
            minlen=len(arr)
            minarray=arr
            
    g.vs[source["index"]]["Motion"]=False
    
    source = g.vs.find(Motion=True)
    resultsswo1 = g.get_all_shortest_paths(source, to='SW0', weights=g.es["weight"], mode='out')
    for arr in resultsswo1:
        if len(arr)<minlen:
            minlen=len(arr)
            minarray=arr
    resultsnwo1 = g.get_all_shortest_paths(source, to='NW0', weights=g.es["weight"], mode='out')
    for arr in resultsnwo1:
        if len(arr)<minlen:
            minlen=len(arr)
            minarray=arr

    resultsseo1 = g.get_all_shortest_paths(source, to='SE0', weights=g.es["weight"], mode='out')
    for arr in resultsseo1:
        if len(arr)<minlen:
            minlen=len(arr)
            minarray=arr
    resultsneo1 = g.get_all_shortest_paths(source, to='NE0', weights=g.es["weight"], mode='out')
    for arr in resultsneo1:
        if len(arr)<minlen:
            minlen=len(arr)
            minarray=arr
            

    return minlen, minarray


def calculateShortExitArrayNew(g,fireSensorArray,motionSensorArray):
    totalresults = []
    alledges = []
    allvertexes=[]
    resString = " "
    '''We put weight for en every edge to be 1000 so
    then we will not pass on that edge'''
    for fireSensor in fireSensorArray:
        if (fireSensor.fireFound):
            g.es[fireSensor.edgeNumber]['weight']=1000
    '''Motion sensor 
    motion sensor array -> pass all sensor array and check if the motion found
    of the motion found and also there is a fire, 
    we need to calculate all exit path'''
    for motionSensor in motionSensorArray:
        if motionSensor.motionFound:
            g.vs["Motion"] = False
            g.vs[motionSensor.idx1Graph]["Motion"]=True
            print("motionSensor.idx2Graph =  ",motionSensor.idx2Graph)
            g.vs[motionSensor.idx2Graph]["Motion"]=True
            minlen, minarray = getgraphshortespathandlen(g)
            print("Motion shortest path ", minarray)
            totalresults.append(minarray)
            resString = resString + " Sensor " + str(motionSensor.sensorNumber) + " path " + str(minarray)
    maxlen = len(totalresults)

    ''' after we find all pathes, we look for the shortest path'''
    for resnum in range (0,maxlen):
        results = totalresults[resnum]
        prev=results[len(results)-1]
        for i in range(len(results)-2,-1,-1):
            num = getedgefrom2vertex(prev,results[i])
            alledges.append(num)
            currentvertex=[]
            currentvertex.append(results[i])
            currentvertex.append(prev)
            allvertexes.append(currentvertex)
            prev = results[i]
    
    return alledges,totalresults
    
            
# def calculateShortExitArray(g,ax,motiogGraph, mylock,motionSensorArray):
#     # add support for motion array
#     totalresults = []
#     mycolorall=[]
#     index = 0
#     resStrcalculateShortExitArraying = " "
#     for motionSensor in motionSensorArray:
#         if motionSensor.motionFound:
#             g.vs["Motion"] = False
#             g.vs[motionSensor.idx1Graph]["Motion"]=True
#             g.vs[motionSensor.idx2Graph]["Motion"]=True
#             minlen, minarray = getgraphshortespathandlen(g)
#             print("Motion shortest path ", minarray)
#             totalresults.append(minarray)
#             mycolorall.append(motionSensor.color)
#             resString = resString + " Sensor " + str(motionSensor.sensorNumber) + " path " + str(minarray)
#             index=index+1
#
#     #todo add drawPath wich receives an array
#     graphDrawer.drawPath(g,ax,motiogGraph, totalresults,mycolorall,mylock,'green')
#     return resString
