# main.py -- put your code here!

import time
import machine
from machine import Pin, PWM
import ujson
import network

from umqttsimple import MQTTClient
from config import MQTT_SERVER, CLIENT_ID, TOPIC_SUB, TOPIC_PUB, LED_LIST
from leds import Leds

import gc
gc.collect()

station = network.WLAN(network.STA_IF)
leds = Leds()

def sub_cb(topic, msg):
  try:
    cmd = ujson.loads(str(msg, 'utf-8'))
    if 'state' in cmd:
      if cmd['state'] == "OFF":
        leds.disableAll()
      else:
        leds.enableAll()
    if 'speed' in cmd:
      leds.steps = int(cmd['fade'])
    if 'color' in cmd:
      for i, (color, _, _) in enumerate(LED_LIST):
        if color in cmd['color']:
          val = int(cmd['color'][color])
          if val >= 0 and val <= 255:
            leds.setColor(i, val)
    if 'reset' in cmd:
      machine.reset()
    
  except Exception as e:
    client.publish(TOPIC_PUB, b"error")


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
  client.set_last_will(TOPIC_PUB, b"offline", retain=False, qos=0)
  client.sock.settimeout(10)
except OSError as e:
  print(e)
  restart_and_reconnect()

last_message = 0
message_interval = 10
counter = 0

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'online #%d' % counter
      client.publish(TOPIC_PUB, msg)
      last_message = time.time()
      gc.collect()
      counter += 1
    leds.update()
    time.sleep(0.02)
  except OSError as e:
    client.publish(TOPIC_PUB, b"OSError")
    restart_and_reconnect()
  if station.isconnected() == False:
    leds.enable(0)
    leds.setColor(0, 60)
    