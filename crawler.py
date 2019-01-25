# -*- coding: utf-8 -*-
from urllib.request import urlopen, Request
from flask import Flask
from flask_socketio import SocketIO, emit
import serial
import struct
import time
import urllib
import bs4
import requests
import threading
import sys
import eventlet
import re
import os
import Adafruit_DHT
import socket
#sys.path.insert(0,'/home/pi/python_docs_samples/vision/cloud_client/face_detection')
#import faces
#import bridge
from datetime import datetime
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app)

global data
global ddata
global dddata
data = []

feelings = [0,0,0,0,0,0,0,0] #'joy','sad','angry','surprise', 'under_exposed', 'blurred', 'headwear','normal'
ip = 'localhost'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_address = (ip, 3000)
#print("line socket listening...")
sock.bind(server_address)

def conn():
    sock.listen(1)
    client, address = sock.accept()
    while 1 :
        re_socket = client.recv(4)
        re_socket = int(re_socket)
        feelings[1]=re_socket
        print("feelings : ")
        print(feelings)
        #socketio.emit('receive',{'data':feelings})

def sayhi():
        global data
        threading.Timer(600.0, sayhi).start()
        location = '인천 용현1.4동'
        enc_location = urllib.parse.quote(location + '+날씨')
        url = 'https://search.naver.com/search.naver?ie=utf8&query='+enc_location
        req = Request(url)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html, 'html5lib')
        temperature = soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text # 기온
        weather = soup.find('p', class_='cast_txt').text # 날씨
        pattern = re.compile(r',')
        [weather,comp_weather]=re.split(pattern,weather)

        mise = soup.find('dl', class_='indicator').text # 미세먼지+초미세먼지+오존지수
        morning = soup.find('li', class_='date_info today').find('span', class_='point_time morning').find('span', class_='rain_rate').find('span', class_='num').text
        afternoon = soup.find('li', class_='date_info today').find('span', class_='point_time afternoon').find('span', class_='rain_rate').find('span', class_='num').text
        print('현재 ' + location + ' 기온은 ' + temperature + '도 입니다.')
        print('날씨는 ' + weather)
#        print(mise)
        pattern = re.compile(r' ')
#        print(re.split(pattern,mise))
        [no1,mi,mi_val,cho,cho_val,ozon,ozon_val,no2] = re.split(pattern,mise);
        print(mi)
        print(mi_val)
        print(cho)
        print(cho_val)
        print(ozon)
        print(ozon_val)
        print('오늘 오전의 강수확률은 '+morning+'% 입니다.')
        print('오늘 오후의 강수확률은 '+afternoon+'% 입니다.')

        data2 = []
        data2.append(temperature)
        data2.append(weather)
        data2.append(comp_weather)
        data2.append(mi)
        data2.append(mi_val)
        data2.append(cho)
        data2.append(cho_val)
        data2.append(ozon)
        data2.append(ozon_val)
        data2.append(morning)
        data2.append(afternoon)
        data = data2

        socketio.emit('mise', {'data': data})

def sayhowhow():
	global ddata
	threading.Timer(60.0, sayhowhow).start()
	humidity, temperature = Adafruit_DHT.read_retry(11,4)
	data3 = []
#data3.append("1")
	data3.append(temperature)
	data3.append(humidity)
	ddata = data3
	print(ddata)
	socketio.emit('inside', {'data': ddata})

class PMS7003(object):

  # PMS7003 protocol data (HEADER 2byte + 30byte)
  PMS_7003_PROTOCOL_SIZE = 32

  # PMS7003 data list
  HEADER_HIGH            = 0  # 0x42
  HEADER_LOW             = 1  # 0x4d
  FRAME_LENGTH           = 2  # 2x13+2(data+check bytes)
  DUST_PM1_0_CF1         = 3  # PM1.0 concentration unit μ g/m3（CF=1，standard particle）
  DUST_PM2_5_CF1         = 4  # PM2.5 concentration unit μ g/m3（CF=1，standard particle）
  DUST_PM10_0_CF1        = 5  # PM10 concentration unit μ g/m3（CF=1，standard particle）
  DUST_PM1_0_ATM         = 6  # PM1.0 concentration unit μ g/m3（under atmospheric environment）
  DUST_PM2_5_ATM         = 7  # PM2.5 concentration unit μ g/m3（under atmospheric environment）
  DUST_PM10_0_ATM        = 8  # PM10 concentration unit μ g/m3  (under atmospheric environment)
  DUST_AIR_0_3           = 9  # indicates the number of particles with diameter beyond 0.3 um in 0.1 L of air.
  DUST_AIR_0_5           = 10 # indicates the number of particles with diameter beyond 0.5 um in 0.1 L of air.
  DUST_AIR_1_0           = 11 # indicates the number of particles with diameter beyond 1.0 um in 0.1 L of air.
  DUST_AIR_2_5           = 12 # indicates the number of particles with diameter beyond 2.5 um in 0.1 L of air.
  DUST_AIR_5_0           = 13 # indicates the number of particles with diameter beyond 5.0 um in 0.1 L of air.
  DUST_AIR_10_0          = 14 # indicates the number of particles with diameter beyond 10 um in 0.1 L of air.
  RESERVEDF              = 15 # Data13 Reserved high 8 bits
  RESERVEDB              = 16 # Data13 Reserved low 8 bits
  CHECKSUM               = 17 # Checksum code

  def header_chk(self, buffer):

    if (buffer[self.HEADER_HIGH] == 66 and buffer[self.HEADER_LOW] == 77):
      return True

    else:
      return False

  # chksum value calculation
  def chksum_cal(self, buffer):

    buffer = buffer[0:self.PMS_7003_PROTOCOL_SIZE]

    chksum_data = struct.unpack('!30BH', buffer)

    chksum = 0

    for i in range(30):
      chksum = chksum + chksum_data[i]

    return chksum

  # checksum check
  def chksum_chk(self, buffer):

    chk_result = self.chksum_cal(buffer)

    chksum_buffer = buffer[30:self.PMS_7003_PROTOCOL_SIZE]
    chksum = struct.unpack('!H', chksum_buffer)

    if (chk_result == chksum[0]):
      return True

    else:
      return False

  # protocol size(small) check
  def protocol_size_chk(self, buffer):

    if(self.PMS_7003_PROTOCOL_SIZE <= len(buffer)):
      return True

    else:
      return False

  # protocol check
  def protocol_chk(self, buffer):

    if(self.protocol_size_chk(buffer)):

      if(self.header_chk(buffer)):

        if(self.chksum_chk(buffer)):

          return True
        else:
          print("Chksum err")
      else:
        print("Header err")
    else:
      print("Protol err")

    return False

  # unpack data
  # <Tuple (13 x unsigned short <H> + 2 x unsigned char <B> + unsigned short <H>)>
  def unpack_data(self, buffer):

    buffer = buffer[0:self.PMS_7003_PROTOCOL_SIZE]

    # data unpack (Byte -> Tuple (13 x unsigned short <H> + 2 x unsigned char <B> + unsigned short <H>))
    data3 = struct.unpack('!2B13H2BH', buffer)

    return data3


  def print_serial(self, buffer):

    chksum = self.chksum_cal(buffer)
    data3 = self.unpack_data(buffer)

    print ("초미세먼지 : %s ug" % (data3[self.DUST_PM2_5_ATM]))
    print ("미세먼지 : %s ug" % (data3[self.DUST_PM10_0_ATM]))
    global dddata
    data4=[]
    data4.append(data3[self.DUST_PM2_5_ATM])
    data4.append(data3[self.DUST_PM10_0_ATM])
    dddata = data4
    socketio.emit('insidedust',{'data':dddata})

USB0 = '/dev/ttyUSB0'
UART = '/dev/ttyAMA0'

SERIAL_PORT = USB0

Speed = 9600

def getDate():
    threading.Timer(1.0, getDate).start()
    global ddddata
    now = datetime.now()
    ddddata=[]
    ddddata.append(now.year)
    ddddata.append(now.month)
    ddddata.append(now.day)
    ddddata.append(now.hour)
    ddddata.append(now.minute)
    ddddata.append(now.second)
    print(ddddata)
    socketio.emit('date',{'data':ddddata})

def getEmotion():
    threading.Timer(60.0, getEmotion).start()
    #print(bridge.hi)
    #socketio.emit('emotion', {'data':bridge.hi})

@socketio.on('mise')
def test_message():
        print('start')
        socketio.emit('mise', {'data':data})

@socketio.on('inside')
def inside():
	socketio.emit('inside', {'data': ddata})

@socketio.on('insidedust')
def insidedust():
	socketio.emit('insidedust', {'data': dddata})

@socketio.on('date')
def date():
    socketio.emit('date',{'data':ddddata})

@socketio.on('receive')
def receive():
    socketio.emit('receive',{'data':feelings})

if __name__== '__main__':
        sayhi()
        sayhowhow()
        getDate()
        #conn()
        #receive_data()
        #getEmotion()
        ser = serial.Serial(SERIAL_PORT,Speed,timeout=1)
        dust = PMS7003()
        ser.flushInput()
        buffer = ser.read(1024)
        if(dust.protocol_chk(buffer)):
	        dust.print_serial(buffer)
        ser.close()
        socketio.run(app)
