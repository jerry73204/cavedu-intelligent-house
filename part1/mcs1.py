import serial
import time
import requests

ser = serial.Serial('/dev/ttyS0',57600)
ser.isOpen()
device_id = "DGDfnSwk"
device_key = "SHKVwfd9mma1YisF"


url_up = "http://api.mediatek.com/mcs/v2/devices/" + device_id
url_up += "/datapoints.csv"

def MCS_upload(dchn,value):
        data = dchn+",,"+str(value)
        r = requests.post(url_up,headers = {"deviceKey" : device_key,'Content-Type':'text/csv'},data=data)
        print r.text

print "Start"

while True:
	a = ""
	try:
		x = ser.inWaiting()
		if x>0:
			for i in range (x):
				a += ser.read()
			
			word = a.split(',')
			if(word[0] == 's'):
		                dis_type  = 'S'
	        	        MCS_upload("disaster_type",dis_type)
		        else:
		                dis_type = word[0]
		                MCS_upload("disaster_type",dis_type)
		                print "danger"
		                print dis_type
	                        
	        	MCS_upload("gas_sensor",word[1])
		        MCS_upload("flame_sensor",word[2])
		        MCS_upload("earthquake_sensor",word[3])
	except requests.exceptions.RequestException as e:
		print e
	time.sleep(1)
