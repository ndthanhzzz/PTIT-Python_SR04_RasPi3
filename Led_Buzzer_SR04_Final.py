#!/usr/bin/python

# Libraries
import RPi.GPIO as GPIO
import time
from time import gmtime, strftime

# Set GPIO Mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Set GPIO Pin
GPIO_BUZZER = 17
GPIO_TRIGGER = 27
GPIO_ECHO = 22
GPIO_RED = 18
GPIO_GREEN = 23
GPIO_BLUE = 24

GPIO.setup(GPIO_RED, GPIO.OUT)
GPIO.setup(GPIO_GREEN, GPIO.OUT)
GPIO.setup(GPIO_BLUE, GPIO.OUT)
GPIO.setup(GPIO_BUZZER, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#distance 
def distance():
  GPIO.output(GPIO_TRIGGER, True) 
  time.sleep(0.1)                                       
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()
  stop = time.time()
  while GPIO.input(GPIO_ECHO) == 0:
    start = time.time()
  while GPIO.input(GPIO_ECHO) == 1:
    stop = time.time()
 
  # Calculate 
  measuredTime = stop - start
  distanceBothWays = measuredTime * 33112 # cm/s 
  distance = distanceBothWays / 2
  print("Distance : {0:5.1f}cm".format(distance), "---------",strftime("%Y-%m-%d %H:%M:%S", gmtime()),"---------")

  return distance

#frequency led distance
def Distance_freq():
  dist = distance()
  if dist > 30:                            # >30cm
    return -1
  elif dist <= 30 and dist >20:            # 20<x<=30
    return 1
  elif dist <= 20 and dist >10:            # 10<x<=20
    return 0.5
  else:                                    #<10
    return 0

# Main function
def main():
  try:
    while True:
      freq = Distance_freq()
      # no beep
      if freq == -1:
        GPIO.output(GPIO_BUZZER, False)
        GPIO.output(GPIO_RED, False) 
        GPIO.output(GPIO_GREEN, False)
        GPIO.output(GPIO_BLUE, False)
        time.sleep(0.25)
      # fast beep
      elif freq == 0:
        GPIO.output(GPIO_BUZZER, True)
        GPIO.output(GPIO_RED, True) 
        time.sleep(0.1) 
        GPIO.output(GPIO_BUZZER, False)
        time.sleep(freq)
        GPIO.output(GPIO_RED, False) 
        
        
        GPIO.output(GPIO_GREEN, False)
        GPIO.output(GPIO_BLUE, False)
      # slow beep
      elif freq == 1:
        GPIO.output(GPIO_BUZZER, True)
        time.sleep(0.1)
        GPIO.output(GPIO_BUZZER, False)
        time.sleep(freq)
        
        GPIO.output(GPIO_RED, False) 
        GPIO.output(GPIO_GREEN, True)
        GPIO.output(GPIO_BLUE, False)
      # normal beep
      else:
        GPIO.output(GPIO_BUZZER, True)
        time.sleep(0.1)
        GPIO.output(GPIO_BUZZER, False)
        time.sleep(freq)
        
        GPIO.output(GPIO_RED, False) 
        GPIO.output(GPIO_GREEN, False)
        GPIO.output(GPIO_BLUE, True)
    
  # If the program is ended, stop beeping and cleanup GPIOs
  except KeyboardInterrupt:
    GPIO.output(GPIO_BUZZER, False)
    GPIO.cleanup()

# Run 
if __name__ == "__main__":
    main()
