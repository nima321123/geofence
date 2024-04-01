
import counterfit_shims_serial
import pynmea2
import time
import json
from azure.eventhub import EventHubProducerClient, EventData
from counterfit_connection import CounterFitConnection

CounterFitConnection.init('127.0.0.1', 5000)

serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')

# Initialize the EventHubProducerClient
producer = EventHubProducerClient.from_connection_string("<storage account connection string>")

def print_gps_data(line):
    msg = pynmea2.parse(line)
    
    if msg.sentence_type == 'GGA':
        lat = pynmea2.dm_to_sd(msg.lat)
        lon = pynmea2.dm_to_sd(msg.lon)

        if msg.lat_dir == 'S':
            lat = lat * -1

        if msg.lon_dir == 'W':
            lon = lon * -1

        # Create a dictionary with the required structure
        gps_data = {
            "gps": {
                "lat": lat,
                "lon": lon
            }
        }

        # Convert the dictionary to a JSON string
        gps_data_json = json.dumps(gps_data)

        print(gps_data_json)

        # Create an EventData instance with the GPS data
        event_data = EventData(gps_data_json)

        # Create a batch
        event_data_batch = producer.create_batch()

        # Add the event data to the batch
        event_data_batch.add(event_data)

        # Send the batch
        producer.send_batch(event_data_batch)

while True:
    line = serial.readline().decode('utf-8')

    while len(line) > 0:
        print_gps_data(line)
        line = serial.readline().decode('utf-8')

    time.sleep(3)
