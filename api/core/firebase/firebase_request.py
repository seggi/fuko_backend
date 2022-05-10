import requests
import json
from decouple import config

FIREBASE_SERVER_TOKEN =  config("FIREBASE_SERVER_TOKEN")

def send_firebase_request():
  serverToken = FIREBASE_SERVER_TOKEN
  deviceToken = 'device token here'

  headers = {
          'Content-Type': 'application/json',
          'Authorization': 'key=' + serverToken,
        }

  body = {
            'notification': {'title': 'Request',
                              'body': 'You are invited to join seggi notebook'
                              },
            'to':
                serverToken,
            'priority': 'high',
          #   'data': dataPayLoad,
          }
  response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
  print(response.status_code)

  return response.json()

  