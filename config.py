import ubinascii
import machine

# Default MQTT server to connect to
mqtt_server = "192.168.1.1"

client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b"Room/rgbBulb/1/command"
topic_pub = b"Room/rgbBulb/1/state"