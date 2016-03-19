#!/usr/bin/env python
          
      
import time
import serial
          
#serial setup, same as read       
ser = serial.Serial(              
	port='/dev/ttyAMA0',
	baudrate = 115200,
	parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
	)
counter=0

#write test          
while 1:
	ser.write('%d'%(counter) + '\r')
	time.sleep(1)
	counter += 1
