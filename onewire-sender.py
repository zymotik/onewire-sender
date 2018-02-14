from w1thermsensor import W1ThermSensor
import sched, time, json, requests, os, sys
import config
import mqtt

schedule = sched.scheduler(time.time, time.sleep)

def collect_temp_readings(sc):
	clear_screen()
	if config.mqtt_enabled:
		mqtt_conn = mqtt.connect_mqtt(config.mqtt_ipaddress, config.mqtt_port, config.mqtt_username, config.mqtt_password)

	readings = []
	for sensor in W1ThermSensor.get_available_sensors():
		sensor_id = int(sensor.id, 16)
		temperature = sensor.get_temperature()
		readings.append({'sensorId': sensor_id, 'ambientTemperature': temperature})
		if config.mqtt_enabled:
			mqtt.publish_temp(mqtt_conn, sensor_id, temperature)

	if config.mqtt_enabled:
		mqtt.disconnect_mqtt(mqtt_conn)

	if config.http_enabled and len(readings) > 0:
		send_to_server(list_to_json(readings))

	if len(readings) == 0:
		print(time.strftime("%H:%M") + " No sensors found.")
	
	schedule.enter(config.poll_period_seconds, 1, collect_temp_readings, (sc,))


def list_to_json(list_obj):
	return json.dumps(list_obj)
	
	
def send_to_server(data_string):
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


print(time.strftime("%H:%M") + " OneWireSender started.")
schedule.enter(config.poll_period_seconds, 1, collect_temp_readings, (schedule,))
schedule.run()