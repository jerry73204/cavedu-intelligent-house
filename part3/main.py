#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time
import logging
import signal
import time
from threading import Thread
import cv2
import RPi.GPIO as GPIO
import auth
import config

# flag indicating if any signal is received
SHUTDOWN_FLAG = False

# the delay time (ms) after each loop
LOOP_DELAY = 0.05

# the timespan that the GPIO pin is set to 1
OUTPUT_PIN_TIMESPAN = 0.03

# do not send warning message for the timespan after the door is opened
DOOR_OPEN_TIMESPAN = 5

# state constants
STATE_OPEN      = 0
STATE_CLOSED    = 1
STATE_INVADED   = 2
STATE_EMERGENCY = 3

# mutable global variables
prev_is_door_open = False
state = STATE_CLOSED

prev_value_train_face = False
prev_value_recognize_face = False
prev_value_auth = False
prev_value_emergency = False
prev_value_invaded = 0

signal_housebreak_timeout = 0
signal_door_not_closed_timeout = 0

door_open_timeout = 0

# utility functions
def is_door_open():
    # TODO implementation
    return False

def is_authenticated():
    global prev_value_auth

    if auth.FLAG_BUSY:
        return False

    value = auth.FLAG_RECOGNITION_RESULT
    result = (prev_value_auth ^ value) & value
    prev_value_auth = value
    return result

def is_signaled_emergency():
    global prev_value_emergency
    value = GPIO.input(config.PIN_IN_EMERGENCY) == 1
    result = (prev_value_emergency ^ value) & value
    prev_value_emergency = value
    return result

def is_signaled_train_face():
    # TODO implementation
    global prev_value_train_face
    value = time.time() % 25 <= 0.3 # dummy impl.
    result = (prev_value_train_face ^ value) & value
    prev_value_train_face = value
    return result

def is_signaled_recognize_face():
    # TODO implementation
    global prev_value_recognize_face
    x = time.time() % 25
    value = x >= 20 and x <= 20.3  # dummy impl.
    result = (prev_value_recognize_face ^ value) & value
    prev_value_recognize_face = value
    return result

def open_door():
    # TODO implementation
    pass

def signal_housebreak():
    global signal_housebreak_timeout
    signal_housebreak_timeout = time.time() + OUTPUT_PIN_TIMESPAN
    GPIO.output(config.PIN_OUT_INVADED, 1)

def signal_door_not_closed():
    global signal_door_not_closed_timeout
    signal_door_not_closed_timeout = time.time() + OUTPUT_PIN_TIMESPAN
    GPIO.output(config.PIN_OUT_TIMEOUT, 1)

# event handlers
def on_auth():
    global door_open_timeout
    global state

    if state == STATE_OPEN:     # ignore this case
        return

    elif state == STATE_CLOSED: # open the door
        door_open_timeout = time.time() + DOOR_OPEN_TIMESPAN
        open_door()
        state = STATE_OPEN

    elif state in (STATE_INVADED, STATE_EMERGENCY): # reset to closed state
        if is_door_open():
            door_open_timeout = time.time() + DOOR_OPEN_TIMESPAN
            state = STATE_OPEN
        else:
            state = STATE_CLOSED

def on_housebreaking():
    logging.debug('event housebreaking')
    global state
    state = STATE_INVADED
    signal_housebreak()

def on_emergency():
    # logging.debug('event emergency')
    global state
    state = STATE_EMERGENCY

def on_door_close():
    logging.debug('event door closed')
    global state
    assert state == STATE_OPEN
    state = STATE_CLOSED

def main():
    global door_open_timeout
    global prev_is_door_open
    global state

    # start authenticator thread
    auth_thread = Thread(target=auth.auth_worker)
    auth_thread.start()

    # initialize
    prev_is_door_open = is_door_open()
    state = STATE_OPEN if prev_is_door_open else STATE_CLOSED

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

        elif state == STATE_OPEN:
            curr_is_door_open = is_door_open()

            if not curr_is_door_open:
                on_door_close()

            elif time.time() >= door_open_timeout:
                door_open_timeout = time.time() + DOOR_OPEN_TIMESPAN
                signal_door_not_closed()

            prev_is_door_open = curr_is_door_open

        elif state == STATE_CLOSED:
            curr_is_door_open = is_door_open()

            if curr_is_door_open:
                on_housebreaking()

            prev_is_door_open = curr_is_door_open

        time.sleep(LOOP_DELAY)

def signal_handler(signum, frame):
    global SHUTDOWN_FLAG
    SHUTDOWN_FLAG = True

if __name__ == '__main__':
    # setup
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    signal.signal(signal.SIGINT, signal_handler)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.PIN_OUT_INVADED, GPIO.OUT)
    GPIO.setup(config.PIN_OUT_TIMEOUT, GPIO.OUT)
    GPIO.setup(config.PIN_IN_EMERGENCY, GPIO.IN)

    GPIO.output(config.PIN_OUT_INVADED, 0)
    GPIO.output(config.PIN_OUT_TIMEOUT, 0)

    # run the main procedure
    logging.info('Access control system started')
    main()
