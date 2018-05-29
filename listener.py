#!/usr/bin/python

import sys
import json
import os
import time
import paho.mqtt.client as mqtt
import logging
import libspacy
import libgrams
import libwordnet
import numpy as np
import numpy
from sklearn import linear_model
import pickle

logging.basicConfig(filename='/tmp/listener.log', level=logging.INFO,format='%(asctime)s %(message)s')

def on_message_new_request(mosq, obj, msg):
  global mqttc
  payload = str(msg.payload)
  logging.info("NEW REQUEST: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
  json_obj = json.loads(payload)
  logging.info(json_obj)


  #All the parameters submitted through the form are available in json_obj
  #This is a simple example
  '''
  exp_id = str(json_obj['id'])
  title = str(json_obj['title'])
  logging.info("id=" + exp_id)
  '''

  #Process the request using any python function
  response_text = 'Hello World'
  response_id = 10
  response_json = {'id':response_id, 'title':response_text}

  response = json.dumps(response_json)

  logging.info("Sending response: "+response)
  topic=exp_id
  mqttc.publish(topic=topic, payload=response)



def get_bizarre_proba(title):
  print "Entered bizarre proba with title=", title

  #load the picke file
  pickle_file = 'log_reg_model.pickle'
  logistic = pickle.load( open( pickle_file, "rb" ) )

  X_test=[]

  print "Extracting features"
  title = ''.join([i if ord(i) < 128 else ' ' for i in title])
  features = generate_features(title)
  X_test.append(features)

  num_features = len(features)
  print "#features=", num_features

  print"Predicting through logistic regression"
  y_pred = logistic.predict_proba(X_test)

  bizarre=round(100*y_pred[0][1])
  return bizarre
 


mqttc = mqtt.Client()
def main():
  global mqttc

# Add message callbacks that will only trigger on a specific subscription match.
  mqttc.message_callback_add("request", on_message_new_request)
  mqttc.connect("localhost", 1883, 60)
  mqttc.subscribe("request", 0)
  print "Subscribed to request"
  mqttc.loop_forever()

if __name__ == "__main__":
  main() 
