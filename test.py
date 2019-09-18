import time
from neopixel import *
import argparse
import numpy as np
import signal

LED_COUNT      = 886      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

FPS = 30
PRODUCTION_MIN = 20
loopCount=0
loop_start_time=0
signal_count=0
period = 1/FPS

def scheduler(arg1,arg2):
   global signal_count
   if signal_count%FPS==0:
      print("now time:"+str(time.time()))
   Light() #call light function
   signal_count=signal_count+1

def Light():
   global loopCount
   loop_start_time=time.time()
   start_index=loopCount*(LED_COUNT+1)
   for j in range(LED_COUNT):
      strip.setPixelColor(j,Color(int(data[start_index+j,1]),int(data[start_index+j,0]),int(data[start_index+j,2])))
      #print(data[j,0])
   strip.show()
   loopCount=loopCount+1
   #print("loop time:"+str(time.time()-loop_start_time))


print("hello")

print("start program")
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
print("file read start")
data = np.genfromtxt("output.txt",delimiter=",", skip_header=0,dtype='int')
print("file read end")

#wait for start
while True:
    input_number=input('>>>')
    if int(input_number)==1:
        break

print("start loop")

signal.signal(signal.SIGALRM, scheduler)
signal.setitimer(signal.ITIMER_REAL, 1, period)

time.sleep(60*PRODUCTION_MIN)
