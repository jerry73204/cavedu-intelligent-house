#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import logging
import signal
import asyncio
import concurrent.futures

import RPi.GPIO as GPIO

import config
import face_auth
import mediatek_cloud

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

# global variables
PREV_DOOR_OPEN = False
PREV_DOOR_CLOSED = False
PREV_VALUE_EMERGENCY = False
PREV_VALUE_TRAIN_FACE = False
PREV_VALUE_RECOGNIZE_FACE = False
PREV_STATE_1 = None
PREV_STATE_2 = None

STATE_CHANGE_TIME = 0

STATE = STATE_CLOSED

FACE_AUTH_SERVICE = None

FUTURE_RECOGNIZE_FACE = None

# utility functions
def run_in_background(func):
    asyncio.get_event_loop().run_in_executor(None, func)

def is_door_open():
    return GPIO.input(config.PIN_IN_MAGNET_SWITCH) == 0

def is_door_opening():
    global PREV_DOOR_OPEN
    value = is_door_open()
    result = (PREV_DOOR_OPEN ^ value) & value
    PREV_DOOR_OPEN = value
    return result

def is_door_closing():
    global PREV_DOOR_CLOSED
    value = not is_door_open()
    result = (PREV_DOOR_CLOSED ^ value) & value
    PREV_DOOR_CLOSED = value
    return result

def is_authenticated():
    return FUTURE_RECOGNIZE_FACE is not None and \
        FUTURE_RECOGNIZE_FACE.done() and \
        FUTURE_RECOGNIZE_FACE.result()

def is_signaled_emergency():
    global PREV_VALUE_EMERGENCY
    value = GPIO.input(config.PIN_IN_EMERGENCY) == 1
    result = (PREV_VALUE_EMERGENCY ^ value) & value
    PREV_VALUE_EMERGENCY = value
    return result

def is_signaled_train_face():
    # TODO implementation
    global PREV_VALUE_TRAIN_FACE
    value = time.time() % 25 <= 0.3 # dummy impl.
    result = (PREV_VALUE_TRAIN_FACE ^ value) & value
    PREV_VALUE_TRAIN_FACE = value
    return result

def is_signaled_recognize_face():
    # TODO implementation
    global PREV_VALUE_RECOGNIZE_FACE
    x = time.time() % 25
    value = x >= 20 and x <= 20.3  # dummy impl.
    result = (PREV_VALUE_RECOGNIZE_FACE ^ value) & value
    PREV_VALUE_RECOGNIZE_FACE = value
    return result

def is_state_changed():
    global PREV_STATE_1
    result = PREV_STATE_1 != STATE
    PREV_STATE_1 = STATE
    return result

def is_state_unchanged():
    global PREV_STATE_2
    result = PREV_STATE_2 == STATE
    PREV_STATE_2 = STATE
    return result

def action_open_door():
    def routine():
        GPIO.output(config.PIN_OUT_LOCK, 1)
        time.sleep(0.5)
        GPIO.output(config.PIN_OUT_LOCK, 0)
    run_in_background(routine)

def action_signal_housebreak():
    def routine():
        GPIO.output(config.PIN_OUT_INVADED, 1)
        time.sleep(0.5)
        GPIO.output(config.PIN_OUT_INVADED, 0)
    run_in_background(routine)

def action_signal_door_not_closed():
    def routine():
        GPIO.output(config.PIN_OUT_TIMEOUT, 1)
        time.sleep(0.5)
        GPIO.output(config.PIN_OUT_TIMEOUT, 0)
    run_in_background(routine)

def action_check_door_open_overtime(expected_state_change_time):
    def routine():
        time.sleep(DOOR_OPEN_TIMESPAN)
        if is_door_open() and STATE_CHANGE_TIME == expected_state_change_time:
            action_signal_door_not_closed()
    run_in_background(routine)

def action_train_face():
    if not FACE_AUTH_SERVICE.schedule_train_face():
        logging.warning('face auth serive is busy')

def action_recognize_face():
    global FUTURE_RECOGNIZE_FACE

    if FUTURE_RECOGNIZE_FACE is None:
        future = concurrent.futures.Future()

        if FACE_AUTH_SERVICE.schedule_recognize_face(future):
            FUTURE_RECOGNIZE_FACE = future
        else:
            logging.warning('face auth serive is busy')

    else:
        logging.warning('previous face recognition task is not finished yet')

# event handlers
def on_auth():
    logging.debug('event auth')
    global STATE

    if STATE == STATE_OPEN:     # ignore this case
        return

    elif STATE in (STATE_CLOSED, STATE_INVADED, STATE_EMERGENCY): # reset to closed state
        action_open_door()
        mediatek_cloud.set_house_status('DOOR OPEN')
        STATE = STATE_OPEN

def on_housebreaking():
    logging.debug('event housebreaking')
    global STATE
    STATE = STATE_INVADED
    mediatek_cloud.set_house_status('INVADED')
    action_signal_housebreak()

def on_emergency():
    logging.debug('event emergency')
    global STATE
    mediatek_cloud.set_house_status('EMERGENCY')
    STATE = STATE_EMERGENCY

def on_door_opening():
    logging.debug('event door_opening')

    if STATE == STATE_CLOSED:
        on_housebreaking()

def on_door_closing():
    global STATE
    logging.debug('event door_closing')

    if STATE == STATE_CLOSED:
        logging.warning('event door_closing is triggered in CLOSED state')

    elif STATE == STATE_OPEN:
        mediatek_cloud.set_house_status('DOOR CLOSED')
        STATE = STATE_CLOSED

def on_state_changed():
    global STATE
    global STATE_CHANGE_TIME

    STATE_CHANGE_TIME = time.time()

    if STATE == STATE_OPEN:
        action_check_door_open_overtime(STATE_CHANGE_TIME)

def on_state_unchanged():
    pass

def main():
    global STATE
    global PREV_STATE_1
    global PREV_STATE_2

    # initialize
    STATE = PREV_STATE_1 = PREV_STATE_2 = STATE_OPEN if is_door_open() else STATE_CLOSED

    # monitor the events by polling
    while True:
        if SHUTDOWN_FLAG:
            logging.info('Shutting down...')
            exit()

        # check events
        if is_signaled_emergency():
            on_emergency()

        elif is_signaled_train_face():
            action_train_face()

        elif is_signaled_recognize_face():
            action_recognize_face()

        elif is_authenticated():
            on_auth()

        elif is_door_opening():
            on_door_opening()

        elif is_door_closing():
            on_door_closing()


        if is_state_changed():
            on_state_changed()

        else:
            on_state_unchanged()

        time.sleep(LOOP_DELAY)

def signal_handler(signum, frame):
    global SHUTDOWN_FLAG
    global FACE_AUTH_SERVICE
    FACE_AUTH_SERVICE.stop()
    SHUTDOWN_FLAG = True

if __name__ == '__main__':
    # setup logger and signal handlers
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    signal.signal(signal.SIGINT, signal_handler)

    # setup GPI Opins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.PIN_OUT_INVADED, GPIO.OUT)
    GPIO.setup(config.PIN_OUT_TIMEOUT, GPIO.OUT)
    GPIO.setup(config.PIN_OUT_LOCK, GPIO.OUT)
    GPIO.setup(config.PIN_IN_EMERGENCY, GPIO.IN)
    GPIO.setup(config.PIN_IN_MAGNET_SWITCH, GPIO.IN)

    GPIO.output(config.PIN_OUT_INVADED, 0)
    GPIO.output(config.PIN_OUT_TIMEOUT, 0)

    # setup face authentication service
    FACE_AUTH_SERVICE = face_auth.FaceAuthServie(config.FACES_DATABASE_PATH)
    FACE_AUTH_SERVICE.start()

    # run the main procedure
    logging.info('Access control system started')
    main()
