# main.py -- put your code here!

import time
import machine
import ujson
import network

from umqttsimple import MQTTClient
from config import MQTT_SERVER, CLIENT_ID, TOPIC_SUB, TOPIC_PUB, LED_LIST
from leds import Leds

import gc
gc.collect()

leds = Leds()
leds.update()

station = network.WLAN(network.STA_IF)

def send_status(error = None):
  msg = {
    'state': "ON" if leds.enabled else "OFF",
    'speed': leds.steps,
    'color': {LED_LIST[i][0]: leds.vals[i] for i in range(len(LED_LIST))},
    'time' : time.time(),
    'error': error
  }
  msg = ujson.dumps(msg)
  client.publish(TOPIC_PUB, bytes(msg, 'utf-8'), retain=True, qos=0)

def sub_cb(topic, msg):
  try:
    cmd = ujson.loads(str(msg, 'utf-8'))
    if 'state' in cmd:
      if cmd['state'] == "OFF":
        leds.disable()
      else:
        leds.enable()
    if 'speed' in cmd:
      leds.setSteps(int(cmd['speed']))
    if 'color' in cmd:
      for i in range(len(LED_LIST)):
        color = LED_LIST[i][0]
        if color in cmd['color']:
          leds.setColor(i, int(cmd['color'][color]))
    if 'reset' in cmd:
      machine.reset()
    send_status()
    
  except Exception as e:
    send_status("cb error")


def connect_and_subscribe():
  client = MQTTClient(CLIENT_ID, MQTT_SERVER)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(TOPIC_SUB)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (MQTT_SERVER, TOPIC_SUB))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
  client.set_last_will(TOPIC_PUB, b"offline", retain=True, qos=0)
  client.sock.settimeout(10)
except OSError as e:
  print(e)
  restart_and_reconnect()

last_message = -55
message_interval = 60

try:
  while True:
    client.check_msg()
    if (time.time() - last_message) >= message_interval:
      send_status()
      last_message = time.time()
      gc.collect()
    leds.update()
    time.sleep(0.02)
    if station.isconnected() == False:
      leds.setColor(0, 60)
except Exception as e:
  try:
    send_status("loop error")
  except:
    print("fatal error")

restart_and_reconnect()
