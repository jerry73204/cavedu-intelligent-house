import serial
import time

ser = serial.Serial(
	port = '/dev/ttyS0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 10
)

#ser = serial.Serial('/dev/ttyS0',timeout=0.5)

while 1:
	rcv = ''
	rcv =  ser.read()
	#print rcv
	
	if rcv == '\x02':
		tag = ""
		while True:
			rcv = ser.read()
			if rcv == '\x03':
				break
			else:
				tag += rcv
		print tag

