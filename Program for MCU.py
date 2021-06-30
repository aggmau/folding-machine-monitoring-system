from umqtt.simple import MQTTClient
from machine import Pin, SPI
import network
import time
import mfrc522

#define pin
led = Pin(2, Pin.OUT)   #LED
sw  = Pin(5, Pin.IN) 	#D1 Reed switch

#define Pin RC522
rdr = mfrc522.MFRC522(14, 13, 12, 0, 4)

#wifi ssid
SSID      = "AgungM21" 
PASSWORD  = "ofiz3095"

#MQTT property
SERVER    = "192.168.43.167"
CLIENT_ID = "yourClientID"
TOPIC     = b"mstekuk1"
username  = 'yourIotUserName'
password  = 'yourIotPassword'
state     = 0
c         = None

#fungsi connect ke WLAN
def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)         #create a wlan object
  wlan.active(True)                         #Activate the network interface
  wlan.disconnect()                         #Disconnect the last connected WiFi
  wlan.connect(ssid,passwd)                 #connect wifi
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)

#fungsi baca RFID
def rfid():
    global tag
    global kondisi
    print("Scan The Workpiece's ID!")
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
      (stat, raw_uid) = rdr.anticoll()
      tag = "%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
      print("New Workpiece detected")
      print(tag)
      kondisi = 2

#fungsi deteksi tuas naik dan kirim pesan
def naik() :
    global kondisi
    global tag
    if sw.value() == 1 :
        #Activate LED
        led.on()
        print('Tuas Naik')
        #kirim pesan ON :
        msg = "%s ON" % (tag)
        c.publish(b"mstekuk1", msg.encode())
        print("Message ON Published")
        #ubah kondisi
        kondisi = 3

#fungsi deteksi tuas turun dan kirim pesan
def turun() :
    global kondisi
    global tag
    if sw.value() == 0 :
        #Activate LED
        led.off()
        print('Tuas Turun')
        #kirim pesan OFF :
        msg = "%s OFF" % ( tag )
        c.publish(b"mstekuk1", msg.encode())
        print("Message OFF Published")
        #ubah kondisi
        kondisi = 1     

#Memulai koneksi WLAN
try:
  connectWifi(SSID,PASSWORD)
  server=SERVER
  c = MQTTClient(CLIENT_ID, server,0,username,password) #create a MQTT client
  c.connect()                                           #connect MQTT
  print("Connected to %s" % (server))

  #main loop
  kondisi = 1
  while True :
      while kondisi == 1 :
          rfid()
      while kondisi == 2 :
          naik()
      while kondisi == 3 :
          turun()

finally:
  if(c is not None):
    c.disconnect()
    wlan.disconnect()
    wlan.active(False)
