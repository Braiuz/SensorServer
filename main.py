from machine import Pin, Timer, reset
from utime import sleep
from dht import DHT11
from led import Led
import micropython          # For emergency exception buffer
import network
import socket

## GLOBAL VAR ##
temperature = 0.0
humidity = 0.0

ssid = "Barbagianni"
password = "ciccinivolantifulminati"

serverIp = "192.168.178.32"
serverPort = "20000"

## Callback ##
def timerCallback(timer):
    global temperature, humidity
    try:
        temperature = (sensor.temperature)
        humidity = (sensor.humidity)
    except Exception as e:
        print("Exception: \"" + str(e)+"\"")

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        sleep(1)
    print(wlan.ifconfig())


## Init ##
print("Pi initialization")
led = Led()

pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

micropython.alloc_emergency_exception_buf(100)      # For emergency exception buffer
timerTask5s = Timer()                               # TODO fai libreria timersw
timerTask5s.init(period=5000, callback=timerCallback)

try:
    connect()
except KeyboardInterrupt:
    reset()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.connect((serverIp, serverPort))



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