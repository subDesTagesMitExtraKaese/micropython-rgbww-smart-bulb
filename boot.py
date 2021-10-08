# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal
print("")
print("    WinnerMicro W600")
print("")

try:
  import machine
  from config import LED_LIST
  for i in range(len(LED_LIST)):
    pin = machine.Pin(LED_LIST[i][1], machine.Pin.OUT, machine.Pin.PULL_DOWN)
    machine.PWM(pin, channel=LED_LIST[i][2], freq=800, duty=100 if i in [0, 4] else 0)

  import network

  station = network.WLAN(network.STA_IF)

  if station.isconnected() == False:
    
    from wifi_config import *
    import easyw600
    easyw600.connect(WIFI_SSID, WIFI_PASSWD)
    easyw600.ftpserver()

except:
  print("boot error")
