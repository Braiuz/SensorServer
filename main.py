from machine import Pin, Timer, reset
from utime import sleep
from dht import DHT11
from led import Led
import micropython          # For emergency exception buffer
import network
import usocket as socket
import utime
from struct import pack

## CONST ##
MSGLEN_BYTE = 24        # int (64) + float (64) + float (64) = 8 + 8 + 8 = 24 byte

## GLOBAL VAR ##
temperature = 0.0
humidity = 0.0
time = 0

ssid = "Barbagianni"
password = "ciccinivolantifulminati"

serverIp = "192.168.178.32"
serverPort = "20000"

## Callback ##
def timerCallback(timer):
    global temperature, humidity, time
    try:
        temperature = (sensor.temperature)
        humidity = (sensor.humidity)
        time = utime.time()
    except Exception as e:
        print("Exception: \"" + str(e)+"\"")

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}", ip)
    return ip


def SocketSend(sock: socket.socket, msg, msgLen):
    totalsent = 0
    while totalsent < msgLen:
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


## Init ##
print("Pi initialization")
led = Led()

pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

micropython.alloc_emergency_exception_buf(100)      # For emergency exception buffer
timerTask5s = Timer()                               # TODO fai libreria timersw
timerTask5s.init(period=5000, callback=timerCallback)

# WLAN connection
try:
    ip = connect()
except KeyboardInterrupt:
    reset()

# Socket init
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Pi initialization done")
## -- ##


## Main loop ##
print("Main loop start")
while True:
    sleep(5)

    print("Temperature: {}".format(temperature))
    print("Humidity: {}".format(humidity))

    # marshal data
    msgBytes = pack('<iff', time, temperature, humidity)

    print(f"Msg len = {len(msgBytes)}")

    clientSocket.connect((serverIp, serverPort))
    print("Connected to: " + serverIp + ":" + serverPort)
    SocketSend(clientSocket, msg=msgBytes, msgLen=len(msgBytes))
    
    led.toogle()

## -- ##