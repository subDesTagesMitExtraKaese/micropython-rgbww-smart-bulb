import ubinascii
import machine

# Default MQTT server to connect to
MQTT_SERVER = "192.168.1.1"

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC_SUB = b"Room/rgbBulb/1/command"
TOPIC_PUB = b"Room/rgbBulb/1/state"

#LEDs with name, pin and channel
LED_LIST = [
  ('R', machine.Pin.PA_05, 0),
  ('G', machine.Pin.PB_13, 1),
  ('B', machine.Pin.PB_15, 3),
  ('C', machine.Pin.PB_16, 2),
  ('W', machine.Pin.PB_08, 4)
]