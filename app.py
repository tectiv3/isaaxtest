# -*- coding: utf-8 -*-
import time, os, requests, json, pprint, commands, string, sys
import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

usr = os.getenv('USER_NAME', '')
pwd = os.getenv('USER_PWD', '')
url = os.getenv('SERVER_URL', '')
if not url:
    print("SERVER_URL is a required variable")
    sys.exit(2)
# data_json = json.dumps({
#     "_route": "sensorlogger.apisensorlogger.registerDevice",
#     "deviceId":"C3D163F9-555C-4E7D-8732-AB4851D041C2",
#     "deviceName":"Multi data sensor",
#     "deviceType": "Indoor",
#     "deviceDataTypes": [
#         {
#             "type": "temperature",
#             "description": "Temperature",
#             "unit": "°C"
#         },
#         {
#             "type": "humidity",
#             "description": "Humidity",
#             "unit": "% r.H."
#         },
#         {
#             "type": "temperature",
#             "description": "CPU",
#             "unit": "°C"
#         }
#     ]
# })
# r = requests.post('https://'+server+'/index.php/apps/sensorlogger/api/v1/registerdevice/',
#     data_json,
#     headers={'Content-Type': 'application/json'},
#     auth=(usr, pwd))
# pprint.pprint(r.json())

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
# ,'temperature': temperature, 'humidity': humidity, 'cpu': cpuTemp,
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Retrying...')
        time.sleep(1.0)
        continue

    cpuTemp = commands.getoutput("vcgencmd measure_temp").split('=')
    cpuTemp = string.replace(cpuTemp[1], "'C", "")
    try:
        response = requests.post(
            url,
            json.dumps({
            'deviceId': 'C3D163F9-555C-4E7D-8732-AB4851D041C2',
            'data': [
              { "dataTypeId": 1, "value": round(temperature, 2) },
              { "dataTypeId": 2, "value": round(humidity, 2) },
              { "dataTypeId": 3, "value": cpuTemp }
            ], 'date': time.strftime("%Y-%m-%d %H:%M:%S")}),
            headers={'Content-Type': 'application/json'},
            auth=(usr, pwd))
#         pprint.pprint(response.json())
    except Exception as e:
        print("Post error:", str(e))
    time.sleep(120.0)
