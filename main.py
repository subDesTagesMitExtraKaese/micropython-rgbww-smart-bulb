# main.py -- put your code here!

import time
import machine
from machine import Pin, PWM
import ujson
import network

from umqttsimple import MQTTClient
from config import mqtt_server, client_id, topic_sub, topic_pub

import gc
gc.collect()

station = network.WLAN(network.STA_IF)

vals = {
  'C': 0,
  'G': 0,
  'R': 0,
  'W': 0,
  'B': 0
}
duration = 50
pwm = {}
def initPWM():
  global pwm
  pwm = {
    'C': PWM(Pin(Pin.PB_16), channel=2, freq=800, duty=vals['C']),
    'G': PWM(Pin(Pin.PB_13), channel=1, freq=800, duty=vals['G']),
    'R': PWM(Pin(Pin.PA_05), channel=0, freq=800, duty=vals['R']),
    'W': PWM(Pin(Pin.PB_08), channel=4, freq=800, duty=vals['W']),
    'B': PWM(Pin(Pin.PB_15), channel=3, freq=800, duty=vals['B'])
  }
initPWM()

def fade():
  global pwm, vals, duration
  if duration > 2:
    diff = {}
    for color in pwm:
      diff[color] = float(vals[color] - pwm[color].duty()) / (duration-1)
    for i in range(duration-1, 1, -1):
      for color in pwm:
        pwm[color].duty(int(vals[color] - diff[color] * i))
      time.sleep(0.02)
  
  for color in pwm:
    pwm[color].duty(vals[color])

def sub_cb(topic, msg):
  global pwm, vals, duration
  try:
    cmd = ujson.loads(str(msg, 'utf-8'))
    if 'state' in cmd:
      if cmd['state'] == "OFF":
        for color in pwm:
          pwm[color].deinit()
        pwm = {}
      else:
        initPWM()
    if 'speed' in cmd:
      duration = int(cmd['fade'])
    if 'color' in cmd:
      for color in vals:
        if color in cmd['color']:
          val = int(cmd['color'][color])
          if val >= 0 and val <= 255:
            vals[color] = val
      fade()
    if 'reset' in cmd:
      machine.reset()
    
  except Exception as e:
    client.publish(topic_pub, b"error")


def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
  client.set_last_will(topic_pub, b"offline", retain=False, qos=0)
  client.sock.settimeout(10)
except OSError as e:
  print(e)
  restart_and_reconnect()

last_message = 0
message_interval = 10
counter = 0

while True:
  try:
    client.wait_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'online #%d' % counter
      client.publish(topic_pub, msg)
      last_message = time.time()
      gc.collect()
      counter += 1
  except OSError as e:
    client.publish(topic_pub, b"OSError")
    restart_and_reconnect()
  if station.isconnected() == False:
    if 'R' in pwm:
      pwm['R'].duty(60)
    