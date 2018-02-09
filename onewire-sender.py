from w1thermsensor import W1ThermSensor
import sched, time, json, requests, os, sys, config

schedule = sched.scheduler(time.time, time.sleep)

print(time.strftime("%H:%M") + " OneWireSender started.")

def collect_temp_readings(sc):
	clear_screen()
	readings = []
	for sensor in W1ThermSensor.get_available_sensors():
		sensor_id = int(sensor.id, 16)
		temperature = sensor.get_temperature()
		readings.append({'sensorId': sensor_id, 'ambientTemperature': temperature})
		if config.mqtt_enabled:
			publish_mqtt(sensor_id, temperature)
	if config.http_enabled and len(readings) > 0:
		send_to_server(list_to_json(readings))

	if len(readings) == 0:
		print(time.strftime("%H:%M") + " No sensors found.")
	
	schedule.enter(config.poll_period_seconds, 1, collect_temp_readings, (sc,))

def publish_mqtt(sensor_id, temperature):
	print('Publish MQTT coming next.')
	print(sensor_id + ':' + temperature)

def list_to_json(list_obj):
	return json.dumps(list_obj)
	
def send_to_server(data_string):
	clear_screen()
	try:
		requests.post(config.http_url, data=data_string, headers=config.http_headers)
		print(data_string)
		print(time.strftime("%H:%M") + " Sent.")
	except:
		print(sys.exc_info()[0])
		print(time.strftime("%H:%M") + " Exception sending data.")
		pass
	
def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')


schedule.enter(config.poll_period_seconds, 1, collect_temp_readings, (schedule,))
schedule.run()
