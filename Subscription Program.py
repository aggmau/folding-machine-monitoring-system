import paho.mqtt.client as mqtt 
import time
import pymysql

def on_connect(client, data, flags, rc):
  print("Connected")
  client.subscribe("mstekuk1")

def on_message(client, data, msg):
  print(msg.topic, msg.payload)
  mdata = msg.payload.decode()
  mdata = mdata.split()
  print("Tag: ", mdata[0], "Status: ", mdata[1])
  con = pymysql.connect("127.0.0.1", "root", "", "mesintekuk")
  print("Connected to database")
  cur = con.cursor()
  if mdata[1] == 'OFF' :
      try:
        cur.execute("UPDATE operation SET action_off = CURRENT_TIMESTAMP() ORDER BY `id_operation` DESC LIMIT 1")
      except:
        print("Error")
  elif mdata[1] == 'ON' :
      try:
        cur.execute("INSERT INTO `operation` (`id_operation`, `id_order`, `id_operator`, `id_workpiece`, `id_machine`, `start_schedule`, `finish_schedule`, `action_on`, `action_off`) VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', current_timestamp(), NULL)" %(id_order, id_operator, mdata[0], id_machine, start_schedule, finish_schedule)) 
      except:
        print("Error")
  con.commit()
  con.close()
  print("Saved")

#data detail order dll
id_order        = 'KAI123'
id_machine      = 'tekuk1'
id_operator     = '53115129'
start_schedule  = '2021-01-01'
finish_schedule = '2021-02-28'

client = mqtt.Client("MyID001")
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
