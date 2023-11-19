from machine import Pin, Timer
from utime import sleep
from dht import DHT11
from led import Led
import micropython          # For emergency exception buffer

## GLOBAL VAR ##
temperature = 0.0
humidity = 0.0


## Callback ##
def timerCallback(timer):
    global temperature, humidity
    try:
        temperature = (sensor.temperature)
        humidity = (sensor.humidity)
    except Exception as e:
        print("Exception: \"" + str(e)+"\"")


## Init ##
print("Pi initialization")
led = Led()

pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

micropython.alloc_emergency_exception_buf(100)      # For emergency exception buffer
timerTask5s = Timer()                               # TODO fai libreria timersw
timerTask5s.init(period=5000, callback=timerCallback)
print("Pi initialization done")
## -- ##


## Main loop ##
print("Main loop start")
while True:
    sleep(5)
    print("Temperature: {}".format(temperature))
    print("Humidity: {}".format(humidity))
    
    led.toogle()

## -- ##