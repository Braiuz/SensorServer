from machine import Pin, Timer, reset
from utime import sleep
from dht import DHT11
from led import Led
import micropython          # For emergency exception buffer
import network
import socket
import utime
from struct import pack

## CONST ##
MSGLEN_BYTE = 12        # int (32) + float (32) + float (32) = 4 + 4 + 4 = 12 byte

## GLOBAL VAR ##
temperature = 0.0
humidity = 0.0
time = 0

ssid = "Barbagianni"
password = "ciccinivolantifulminati"

serverIp = "192.168.178.32"
serverPort = 2500
DISCONNECT_MESSAGE = "!DISCONNECT!"
FORMAT = 'utf-8'

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
    print(f"Connected to wlan on {ip}")
    return ip


def SocketSend(sock: socket.socket, msg, msgLen):
    totalsent = 0
    while totalsent < msgLen:
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
    print("Sent " + str(msg) + ", "+ str(totalsent) + " bytes")


## Init ##
print("Pi initialization")
led = Led()

pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

micropython.alloc_emergency_exception_buf(100)      # For emergency exception buffer
timerTask5s = Timer()                               # TODO fai libreria timersw
#timerTask5s.init(period=5000, callback=timerCallback)

connected = False   # state of connection with server

# WLAN connection
try:
    ip = connect()
except KeyboardInterrupt:
    reset()

# Socket init
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Pi initialization done")
sleep(1)
## -- ##


## Main loop ##
print("Main loop start")
while True:
    print("Temperature: {}".format(temperature))
    print("Humidity: {}".format(humidity))

    # marshal data
    msgBytes = pack('<iff', time, temperature, humidity)

    #print(f"Msg len = {len(msgBytes)}")

    try:
        clientSocket.connect((serverIp, serverPort))

        print("\nConnected to server: " + serverIp + ":" + str(serverPort))
        print("Message = " + str(msgBytes))
        SocketSend(clientSocket, msg=msgBytes, msgLen=len(msgBytes))
        sleep(5)
        print("Sending disconnect message")
        SocketSend(clientSocket, msg=DISCONNECT_MESSAGE.encode(FORMAT), msgLen=len(DISCONNECT_MESSAGE))   # gli dico di disconnettersi
        clientSocket.recv(MSGLEN_BYTE)          # se recv esce con 0 byte ricevuti allora la connessione è stata chiusa --> posso rifare la connect
    except OSError as e:
         print("Exception: " + str(e))
    # finally:
    #     clientSocket.close()
    #     connected = False
    
    led.toogle()
    sleep(5)
## -- ##