#!/usr/bin/env python
                
import time
import serial      

#realine handler on all possible string ends, may return empty string
def readlineCR(port):
        rv = ""
        while True:
        	ch = port.read()
        	rv += ch
        	if ch == '\r' or ch == '' or ch == '\n':
             		return rv

#serial setup for raspberryPi, read timeout: 1 second                
ser = serial.Serial(              
	port='/dev/ttyAMA0',
	baudrate = 115200,
	parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
	timeout = 1
	)

#read and print
while 1:
	rcv = readlineCR(ser)
	print(rcv)
