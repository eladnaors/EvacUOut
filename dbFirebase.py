import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
from datetime import datetime
global db

db=None
''' Opens the connection to the firebase DB
uses json file "evacuout" to connect to the firebase
'''
def firebaseDB():
    global db
    if db is None:
        cred = credentials.Certificate("evacuout-firebase-adminsdk-f7wop-c59a235322.json")
        app=firebase_admin.initialize_app(cred)
        db = firestore.client()

    return db

'''saves motion sensor to db'''
def savemotionSensors(db,motionSensors):
    
    for motionSensor in motionSensors:
        #print("type(motionSensor)", type(motionSensor))
        motionSensor.timeStampS = datetime.fromtimestamp(time.time())
        db.collection(u'motionSensor').document(motionSensor.sensorID).set(motionSensor.tojson)

'''saves fire sensor to db'''
def savefireSensors(db,fireSensors):
    
    for fireSensor in fireSensors:
        fireSensor.timeStampS = datetime.fromtimestamp(time.time())
        db.collection(u'fireSensor').document(fireSensor.sensorID).set(fireSensor.tojson)

'''clear firebase db, every time rasbery starts'''
def clearDB(isRasber):
   if isRasber == True:       
        docs = db.collection('motionSensor').list_documents(page_size=100)
        deleted = 0
        for doc in docs:
            print(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
            doc.delete()
        docs = db.collection('fireSensor').list_documents(page_size=100)
        deleted = 0
        for doc in docs:
            print(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
            doc.delete()
    