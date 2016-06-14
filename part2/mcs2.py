import serial
import time
import requests

ser = serial.Serial('/dev/ttyS0',57600)
ser.isOpen()
device_id = "DGDfnSwk"
device_key = "SHKVwfd9mma1YisF"


url_up = "http://api.mediatek.com/mcs/v2/devices/" + device_id
url_up += "/datapoints.csv"

lastliv = '0'
lastcolor = '0'

def MCS_upload(dchn,value):
	try:
	        data = dchn+",,"+str(value)
	        r = requests.post(url_up,headers = {"deviceKey" : device_key,'Content-Type':'text/csv'},data=data)
	        print r.text
	except requests.exceptions.RequestException as e:
		print e

def MCS_read(dchn):
	try:
	        url_rd = "http://api.mediatek.com/mcs/v2/devices/" + device_id 
	        url_rd += "/datachannels/" + dchn + "/datapoints.csv"
	        r = requests.get(url_rd, headers = {"deviceKey" : device_key})
	        data = r.content.split(',')[2:]
	        #print data
	        return data
	except requests.exceptions.RequestException as e:
                print e
print "Start"
while True:

	a = ""
        liv = MCS_read("livingroom")

        if liv[0] !=lastliv:
                if liv[0] == '1':
                        print "livingroom on"
                        ser.write("lo\r")
                else:
                        print "livingroom off"
                        ser.write("lc\r")
        lastliv = liv[0]

        color = MCS_read("living_color")

        if color[0] !=lastcolor:
                print color[0]
                ser.write("c"+color[0]);
                
        lastcolor = color[0]
	
	x = ser.inWaiting()
	print x	

        if x>0:
		for i in range(x):
			a +=ser.read()
		print a
                sensor = a.split(',') #light,inside,outside,solar
		print sensor
		
		if sensor[0] == 'S':
			print "safe"
		elif sensor[0] == 'D':
			print "danger"
                elif int(sensor[0])>=0 :
                	MCS_upload("blackout",sensor[0])
	                MCS_upload("inside_degree",sensor[1])
	                MCS_upload("outside_degree",sensor[2])
	                MCS_upload("solar",sensor[3])
		else:
			print "Arduino send error!"
	time .sleep(1)

