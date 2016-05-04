import serial

import config

SERIAL_RFID = serial.Serial(
    port=config.SERIAL_DEVICE_PATH,
    baudrate=config.SERIAL_BAUDRATE,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=10
)

def read_tag():
    rcv = SERIAL_RFID.read()

    if rcv == '\x02':
        tag = ''
        while True:
            rcv = SERIAL_RFID.read()
            if rcv == '\x03':
                break
            else:
                tag += rcv
        return tag
    else:
        return None
