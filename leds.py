import time
from machine import PWM, Pin

from config import LED_LIST

class Leds:
  def __init__(self):
    self.led_count = len(LED_LIST)
    self.pwm = [None] * self.led_count
    self.vals = [x[3] for x in LED_LIST]
    self.diff = [0] * self.led_count
    self.stepId = [0] * self.led_count
    self.steps = 50
    self.frequency = 800
    self.enabled = True
  
  def init(self, i):
    if not self.pwm[i]:
      self.pwm[i] = PWM(Pin(LED_LIST[i][1]), channel=LED_LIST[i][2], freq=self.frequency, duty=0)

  def deinit(self, i):
    if self.pwm[i]:
      self.pwm[i].deinit()
      self.pwm[i] = None

  def enable(self):
    self.enabled = True
    for i in range(self.led_count):
      self.diff[i] = float(self.vals[i]) / self.steps
      self.stepId[i] = 0

  def disable(self):
    for i in range(self.led_count):
      self.setColor(i, 0)
    self.enabled = False

  def setSteps(self, n):
    if n < 1:
      n = 1
    self.steps = n

  def setColor(self, i, val):
    if val < 0:
      val = 0
    elif val > 256:
      val = 256
    self.vals[i] = val

    if not self.enabled:
      return
    if not self.pwm[i]:
      self.diff[i] = self.vals[i]
    else:
      self.diff[i] = self.vals[i] - (self.pwm[i].duty() + 1)
    self.stepId[i] = 0

  def update(self):
    for i in range(self.led_count):
      if self.enabled and not self.pwm[i] and self.vals[i]:
        self.init(i)
      elif not self.pwm[i]:
        continue
      if self.stepId[i] > self.steps:
        self.diff[i] = 0
        if self.vals[i] == 0 or not self.enabled:
          self.deinit(i)
      else:
        if self.enabled:
          val = int(self.vals[i] - self.diff[i] * float(self.steps - self.stepId[i]) / self.steps) - 1
        else:
          val = int(-self.diff[i] * float(self.steps - self.stepId[i]) / self.steps)
        if val < 0:
          val = 0
        if val > 255:
          val = 255
        self.pwm[i].duty(val)
        self.stepId[i] += 1
  