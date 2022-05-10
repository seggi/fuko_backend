import requests
import json

def send_firebase_request():
  serverToken = 'AAAAP_Wvopg:APA91bFWlJDVk8LWeWy5biHGWL6XaThNmu753bw2G1l7De_ddcPHA_fPlKQip6tCLieGC0LnyAPe6tfJgiAhSQlLgFhGNblKiwlByrqQQUQSOMQ2BStbAVQI_Z7dWrJEquSbjsdGnnxq'
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

  