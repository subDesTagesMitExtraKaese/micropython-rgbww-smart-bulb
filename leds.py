import time
from machine import PWM, Pin

from config import LED_LIST

class Leds:
  def __init__(self):
    self.led_count = len(LED_LIST)
    self.pwm = [None] * self.led_count
    self.vals = [0] * self.led_count
    self.diff = [0.0] * self.led_count
    self.stepId = [0] * self.led_count
    self.steps = 50
    self.frequency = 800
  
  def enable(self, i):
    if not self.pwm[i]:
      self.pwm[i] = PWM(Pin(LED_LIST[i][1]), channel=LED_LIST[i][2], freq=self.frequency, duty=0)

  def enableAll(self):
    for i in range(self.led_count):
      self.enable(i)

  def disable(self, i):
    if self.pwm[i]:
      self.pwm[i].deinit()
      self.pwm[i] = None

  def disableAll(self):
    for i in range(self.led_count):
      self.disable(i)

  def setColor(self, i, val):
    if not self.pwm[i]:
      return
    self.diff[i] = float(self.vals[i] - self.pwm[i].duty()) / (self.steps)
    self.vals[i] = val
    self.stepId[i] = 0

  def update(self):
    for i in range(self.led_count):
      if not self.pwm[i]:
        continue
      if self.stepId[i] > self.steps:
        self.pwm[i].duty(self.vals[i])
      else:
        self.pwm[i].duty(int(self.vals[i] - self.diff[i] * (self.steps - self.stepId[i])))
        self.stepId[i] += 1
  