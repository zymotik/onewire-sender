from w1thermsensor import W1ThermSensor
import sched, time, json, requests, os, sys

wait = 60
api_url = "https://your-endpoint.com/api/sensorslog"

s = sched.scheduler(time.time, time.sleep)

print(time.strftime("%H:%M") + " OneWireSender started.")

def publish_temp_readings(sc):
	readings = [];
	for sensor in W1ThermSensor.get_available_sensors():
		readings.append({'sensorId': int(sensor.id, 16), 'ambientTemperature': sensor.get_temperature()})
	
	if len(readings) > 0:
		send_to_server(list_to_json(readings))
	else:
		clear_screen()
		print(time.strftime("%H:%M") + " No sensors found.")
	
	s.enter(wait, 1, publish_temp_readings, (sc,))

def list_to_json(list_obj):
	return json.dumps(list_obj)
	
def send_to_server(data_string):
	headers = { "Content-Type": "application/json" }
	try:
		r = requests.post(api_url, data=data_string, headers=headers)
		clear_screen()
		print(data_string);
		print(time.strftime("%H:%M") + " Sent.")
	except:
		clear_screen()
		print(sys.exc_info()[0])
		print(time.strftime("%H:%M") + " Exception sending data.")
		pass
	
def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')


s.enter(wait, 1, publish_temp_readings, (s,))
s.run()
