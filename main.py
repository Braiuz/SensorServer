from machine import Pin
from utime import sleep
from dht import DHT11
from led import Led

from machine import Pin

led = Led()

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