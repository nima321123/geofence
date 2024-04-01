# Azure Function for Geofence Alerting

This project contains an Azure Function that triggers on new events in an Azure Event Hub. The function checks if the GPS coordinates in the event data are inside a predefined geofence. If the point is inside the geofence, an email alert is sent.

## How it works

1. The function triggers on new events in the Event Hub named "geofeventhub".
2. The function parses the event data (expected to be JSON) and extracts the latitude and longitude from the `gps` field.
3. The function makes a GET request to the Microsoft Atlas Geofence API to check if the point is inside the geofence.
4. If the point is inside the geofence, the `send_email` function is called, which sends an email using the Mailgun API.

## Prerequisites

- Azure account
- Azure Event Hub named "geofeventhub"
- Microsoft Atlas Geofence API set up with a valid `MAPS_KEY` and `GEOFENCE_UDID`
- Mailgun account with a valid `MAILGUN_DOMAIN`, `MAILGUN_FROM_EMAIL`, and `MAILGUN_API_KEY`

## Deployment
1. Set up Counterfit. Modify your app.py code as in the counterfit_app.py file on this repository
2. Set the necessary environment variables (`MAILGUN_DOMAIN`, `MAILGUN_FROM_EMAIL`, `MAILGUN_API_KEY`, `MAPS_KEY`, `GEOFENCE_UDID`) in the application settings of your Azure Functions app.
3. Run the function locally using Azurite.
4. Deploy the function to Azure Functions.

## Usage

Send events to the "geofeventhub" Event Hub. The events should be JSON objects with a `gps` field containing `lat` and `lon` fields for the latitude and longitude, respectively.

