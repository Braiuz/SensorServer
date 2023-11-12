from machine import Pin, Timer
from utime import sleep
from dht import DHT11
from led import Led
import micropython          # For emergency exception buffer

## Init ##
led = Led()
micropython.alloc_emergency_exception_buf(100)      # For emergency exception buffer
timerTask1ms = Timer()                              # TODO fai libreria timersw
## -- ##

while True:
    try:
        sleep(5)
        pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
        sensor = DHT11(pin)
        t  = (sensor.temperature)
        h = (sensor.humidity)
        print("Temperature: {}".format(sensor.temperature))
        print("Humidity: {}".format(sensor.humidity))
    except Exception as e:
        print("Exception: \"" + str(e)+"\"")
    
    led.toogle()