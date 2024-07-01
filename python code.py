#Importing necessary libraries
import conf
from boltiot import Bolt
import json
import time
import re
import requests


# Initialize Bolt Details
api_key = conf.bolt_api_key
device_id = conf.device_id
bolt = Bolt(api_key, device_id)

# Telegram details
telegram_bot_id = conf.telegram_bot_id
telegram_chat_id = conf.telegram_chat_id

# Initialize the regular expression pattern for parsing sensor data
sensor_data_pattern = re.compile(r"Y: (-?\d+\.\d+), Z: (-?\d+\.\d+), Xacc:(-?\d+\.\d+), Temperature: (\d+\.\d+), Humidity: (\d+\.\d+)")

def fetch_data():
    response = bolt.serialRead('10')
    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return None

    if data["success"] != 1:
        print("Error:", data["value"])
        return None
    return data["value"]

def parse_sensor_data(sensor_data):
    match = sensor_data_pattern.search(sensor_data)
    if match:
        # Extract values
        Y = float(match.group(1))
        Z = float(match.group(2))
        Xacc = float(match.group(3))
        Temperature = float(match.group(4))
        Humidity = float(match.group(5))

        # Check thresholds and send telegram message if exceeded
        if (Temperature > 40 or Humidity > 70 or Xacc > 4 or Y > 4 or Z > 12):
            message = f"Warning! Threshold exceeded:\n" \
                      f"Y: {Y}, Z: {Z}, Xacc: {Xacc}, Temperature: {Temperature}, Humidity: {Humidity}"
            send_telegram_message(message)

        return {
            "Y": Y,
            "Z": Z,
            "Xacc": Xacc,
            "Temperature": Temperature,
            "Humidity": Humidity
        }
    else:
        print("Error: Unable to parse sensor data")
        return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_bot_id}/sendMessage"
    data = {"chat_id": telegram_chat_id, "text": message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    else:
        print("Message sent successfully!")

# Initial delay to allow system to stabilize
#this is not necessary I am using it just because my initial values were missing without initial delay.
print("Starting data collection after initial delay...")
time.sleep(10)

# Initial flush of serial buffer
#not necessary
print("Flushing initial reads...")
for _ in range(5):
    fetch_data()
    time.sleep(1)

while True:
    sensor_data = fetch_data()
    if sensor_data:
        print(f"Raw sensor data: {sensor_data}")
        parsed_data = parse_sensor_data(sensor_data)
        if parsed_data:
            # Print the parsed data (optional)
            print(parsed_data)

    time.sleep(5)  # Adjust delay as needed
