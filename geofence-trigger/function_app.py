import azure.functions as func
import datetime
import json
import logging
import os
import requests

app = func.FunctionApp()

def send_email(subject, message):
    recipient_email = "10422015@student.vgu.edu.vn"
    logging.info('send_email function called')  
    url = f"https://api.mailgun.net/v3/{os.environ['MAILGUN_DOMAIN']}/messages"

    data = {
        "from": os.environ['MAILGUN_FROM_EMAIL'],
        "to": recipient_email,
        "subject": subject,
        "text": message
    }

    response = requests.post(url, auth=("api", os.environ['MAILGUN_API_KEY']), data=data)

    if response.status_code != 200:
        logging.error(f'Error sending email: {response.content}')

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="geofeventhub",
                               connection="EventHubConnectionString") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    maps_key = os.environ['MAPS_KEY']
    geofence_udid = os.environ['GEOFENCE_UDID']
    recipient_email = os.environ['RECIPIENT_EMAIL']

    event_data = azeventhub.get_body().decode('utf-8')
    event_data = event_data.strip()

    if event_data.startswith('{') and event_data.endswith('}'):
        event_bodies = [json.loads(event_data)]
    else:
        # Handle multiple JSON objects
        event_bodies = [json.loads(obj) for obj in event_data.split('\n') if obj.strip()]

    for event_body in event_bodies:
        lat = event_body['gps']['lat']
        lon = event_body['gps']['lon']

        url = 'https://atlas.microsoft.com/spatial/geofence/json'

        params = {
            'api-version': 1.0,
            'deviceId': 'gps-sensor',
            'subscription-key': maps_key,
            'udid' : geofence_udid,
            'lat' : lat,
            'lon' : lon
        }

        response = requests.get(url, params=params)
        response_body = json.loads(response.text)

        distance = response_body['geometries'][0]['distance']

        if distance == 999:
            logging.info('Point is outside geofence')
        elif distance > 0:
            logging.info(f'Point is just outside geofence by a distance of {distance}m')
        elif distance == -999:
            logging.info(f'Point is inside geofence')
            send_email('IoT Alert: Point is inside geofence', 'The point is inside the geofence.')
        else:
            logging.info(f'Point is just inside geofence by a distance of {distance}m')
