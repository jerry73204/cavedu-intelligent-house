#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time
import logging
import signal
from threading import Thread
import serial
import cv2
import auth
import config

# flag indicating if any signal is received
SHUTDOWN_FLAG = False

# the delay time (ms) after each loop
LOOP_DELAY = 0.05

# state constants
STATE_OPEN      = 0
STATE_CLOSED    = 1
STATE_INVADED   = 2
STATE_EMERGENCY = 3

# mutable global variables
serial_device = serial.Serial(port=config.SERIAL_DEVICE_PATH,
                              baudrate=config.SERIAL_BAUDRATE,
                              parity=serial.PARITY_NONE,
                              stopbits=serial.STOPBITS_ONE,
                              bytesize=serial.EIGHTBITS,
                              timeout=0)

prev_door_state = False
state = STATE_CLOSED

last_time_signaled_train_face = 0
last_time_signaled_recognize_face = 0

# utility functions
def is_door_open():
    # TODO implementation
    return False

def is_authenticated():
    if not auth.FLAG_BUSY:
        if auth.FLAG_RECOGNITION_RESULT:
            auth.FLAG_RECOGNITION_RESULT = False
            return time.time() <= auth.LAST_RECOGNITION_TIME + 5
        else:
            return False

def is_signaled_emergency():
    payload = serial_device.read(size=65536)
    return len(payload) > 0

def is_signaled_train_face():
    # TODO implementation
    global last_time_signaled_train_face
    if time.time() < last_time_signaled_train_face + 1:
        return False

    result = time.time() % 25 <= 0.3 # dummy impl.
    if result:
        last_time_signaled_train_face = time.time()

    return result

def is_signaled_recognize_face():
    # TODO implementation
    global last_time_signaled_recognize_face
    if time.time() < last_time_signaled_recognize_face + 1:
        return False

    x = time.time() % 25
    result = x >= 20 and x <= 20.3  # dummy impl.
    if result:
        last_time_signaled_recognize_face = time.time()

    return result

def open_door():
    # TODO implementation
    pass

def warn_invaded():
    serial_device.write('I')

# event handlers
def on_auth():
    global state

    if state == STATE_OPEN:     # ignore this case
        return

    elif state == STATE_CLOSED: # open the door
        open_door()
        state = STATE_OPEN

    elif state in (STATE_INVADED, STATE_EMERGENCY): # reset to closed state
        state = STATE_CLOSED

def on_housebreaking():
    logging.debug('event housebreaking')
    global state
    state = STATE_INVADED
    warn_invaded()

def on_emergency():
    logging.debug('event emergency')
    global state
    state = STATE_EMERGENCY

def on_door_close():
    logging.debug('event door closed')
    global state
    assert state == STATE_OPEN
    state = STATE_CLOSED

def main():
    global prev_door_state
    global state

    # start authenticator thread
    auth_thread = Thread(target=auth.auth_worker)
    auth_thread.start()

    # initialize
    prev_door_state = is_door_open()
    state = STATE_OPEN if prev_door_state else STATE_CLOSED

    # monitor the events by polling
    while True:
        if SHUTDOWN_FLAG:
            logging.info('Shutting down...')
            auth.FLAG_SHUTDOWN = True
            auth_thread.join()
            exit()

        elif is_signaled_emergency():
            on_emergency()

        elif is_signaled_train_face():
            auth.FLAG_TRAIN_REQUEST = True

        elif is_signaled_recognize_face():
            auth.FLAG_RECOGNITION_REQUEST = True

        elif is_authenticated():
            on_auth()

        else:
            curr_door_state = is_door_open()

            if curr_door_state != prev_door_state:
                if curr_door_state:
                    on_housebreaking()
                else:
                    on_door_close()

            prev_door_state = curr_door_state

        time.sleep(LOOP_DELAY)

def signal_handler(signum, frame):
    global SHUTDOWN_FLAG
    SHUTDOWN_FLAG = True

if __name__ == '__main__':
    # setup
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    signal.signal(signal.SIGINT, signal_handler)

    # run the main procedure
    logging.info('Access control system started')
    main()
