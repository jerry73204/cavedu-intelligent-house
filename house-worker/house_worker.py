#!/usr/bin/env python2
import os
import re
import sys
import json
import argparse
import socket
import select
import signal
import struct
from threading import Thread
import logging

import serial

DEVICE_TYPE_DUMMY = 0
DEVICE_TYPE_MT_7688 = 1
DEVICE_TYPE_MT_7688_DUO = 2
DEVICE_TYPE_PI_1 = 3
DEVICE_TYPE_PI_2 = 4
DEVICE_TYPE_PI_3 = 5

SERVER_SOCKETS = list()
SERIAL_DEVICES = list()
OPENED_FILES = list()
USE_STANDARD_IO = False
DEVICE_TYPE = None

SELECT_TIMEOUT = 1
FLAG_SHUTDOWN = False

def signal_handler(signum, frame):
    global FLAG_SHUTDOWN
    FLAG_SHUTDOWN = True

def handle_request(data):
    action = data['action']

    def action_gpio_read():
        pass

    def action_gpio_write():
        pass

    def action_i2c_read():
        pass

    def action_i2c_write():
        pass

    def action_serial_read():
        pass

    def action_serial_write():
        pass

    if action == 'gpio_read':
        return action_gpio_read()

    elif action == 'gpio_write':
        return action_gpio_write()

    elif action == 'i2c_read':
        return action_i2c_read()

    elif action == 'i2c_write':
        return action_i2c_write()

    elif action == 'serial_read':
        return action_serial_read()

    elif action == 'serial_write':
        return action_serial_write()

def client_handler(reader, writer):
    state_read_size = 1
    state_read_content = 2
    state_write = 3

    state = state_read_size
    size_left = 4

    read_buffer = ''
    write_buffer = ''

    def finalize():
        if 'close' in dir(reader):
            reader.close()
        else:
            os.close(reader.fileno())

        if 'close' in dir(writer):
            writer.close()
        else:
            os.close(writer.fileno())


    while not FLAG_SHUTDOWN:
        if state in (state_read_size, state_read_content):
            try:
                if len(select.select([reader], list(), list(), SELECT_TIMEOUT)[0]) == 0:
                    continue
            except select.error as e:
                if e[0] == 4:   # check interrupted system call
                    finalize()
                    return

            payload = os.read(reader.fileno(), size_left)
            if len(payload) == 0: # check if the file is closed or reaches EOF
                if size_left != 4:
                    logging.warning('connection lost while request is not complete')

                finalize()
                return

            size_left -= len(payload)
            read_buffer += payload

            if size_left == 0:
                if state == state_read_size:
                    request_size = struct.unpack('<I', read_buffer)[0]

                    if request_size > 0:
                        size_left = request_size
                        read_buffer = ''
                        state = state_read_content
                    else:
                        size_left = 4
                        read_buffer = ''

                else:           # case state == state_read_content
                    try:
                        request_data = json.loads(read_buffer)
                    except ValueError: # check if this string can be decoded as JSON object
                        logging.warning('corrupted request detected. connection closed')
                        finalize()
                        return

                    response = handle_request(request_data)
                    write_buffer = json.dumps(response)
                    write_buffer = struct.pack('<I', len(write_buffer)) + write_buffer
                    state = state_write

        elif state == state_write:
            try:
                if len(select.select(list(), [writer], list(), SELECT_TIMEOUT)[1]) == 0:
                    continue
            except select.error as e: # check interrupted system call
                if e[0] == 4:
                    finalize()
                    return

            written_size = os.write(writer.fileno(), write_buffer)
            write_buffer = write_buffer[written_size:]

            if len(write_buffer) == 0:
                size_left = 4
                read_buffer = ''
                state = state_read_size

def main():
    global DEVICE_TYPE

    def init_dummy():
        logging.info('running on a dummy device')

    def init_MT7688():
        logging.info('running on a MediaTek 7688 device')
        import mraa

    def init_MT7688_Duo():
        logging.info('running on a MediaTek 7688 Duo device')
        import mraa

    def init_Pi1():
        logging.info('running on a Raspberry Pi device')
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)


    def init_Pi2():
        logging.info('running on a Raspberry Pi 2 device')
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)

    def init_Pi3():
        logging.info('running on a Raspberry Pi 3 device')
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)

    global USE_STANDARD_IO

    # setups
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    signal.signal(signal.SIGINT, signal_handler)

    # argument specification
    arg_parser = argparse.ArgumentParser(description='CAVEDU intelligent house client')
    arg_parser.add_argument('--device',
                            required=True,
                            metavar='DEVICE_TYPE',
                            choices=['dummy', 'MT7688', 'MT7688_Duo', 'Pi1', 'Pi2', 'Pi3'],
                            nargs=1,
                            help='specify the device model. DEVICE_TYPE can be either MT7688, MT7688_Duo, Pi1, Pi2, Pi3')
    arg_parser.add_argument('--serial',
                            metavar=('SERIAL_PATH', 'BAUDRATE'),
                            nargs=2,
                            action='append',
                            help='use serial communication. eg. --serial /dev/ttyAMA0')
    arg_parser.add_argument('--network',
                            metavar='HOST:PORT',
                            nargs=1,
                            action='append',
                            help='use network communicatoin over a TCP connection, HOST is optional. eg. --network 22177, --network 127.0.0.1:22177')
    arg_parser.add_argument('--file',
                            metavar='FILE',
                            nargs=1,
                            action='append',
                            help='treat FILE as a communication channel')
    arg_parser.add_argument('--standard-io',
                            action='store_true',
                            help='treat standard input, standard output as a communication channel')
    args = arg_parser.parse_args()

    # parse arguments
    if args.device[0] == 'dummy':
        DEVICE_TYPE = DEVICE_TYPE_DUMMY
        init_dummy()

    elif args.device[0] == 'MT7688':
        DEVICE_TYPE = DEVICE_TYPE_MT_7688
        init_MT7688()

    elif args.device[0] == 'MT7688_Duo':
        DEVICE_TYPE = DEVICE_TYPE_MT_7688_DUO
        init_MT7688_Duo()

    elif args.device[0] == 'Pi1':
        DEVICE_TYPE = DEVICE_TYPE_PI_1
        init_Pi1()

    elif args.device[0] == 'Pi2':
        DEVICE_TYPE = DEVICE_TYPE_PI_2
        init_Pi2()

    elif args.device[0] == 'Pi3':
        DEVICE_TYPE = DEVICE_TYPE_PI_3
        init_Pi3()

    else:
        exit(2)

    if args.network is not None:
        for arg in args.network:
            _, host, port = re.findall(r'^(([^:]+):)?(\d{1,5})$', arg[0])[0]
            port = int(port)

            if port > 65535:
                exit(2)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host, port))
            sock.listen(5)
            SERVER_SOCKETS.append(sock)


    if args.serial is not None:
        for arg in args.serial:
            serial_path, baudrate = arg
            baudrate = int(baudrate)

            serial_device = serial.Serial(serial_path, baudrate=baudrate)
            SERIAL_DEVICES.append(serial_device)

    if args.file is not None:
        for arg in args.file:
            file_path = arg[0]
            opened_file = open(file_path, 'rwb')
            OPENED_FILES.append(opened_file)

    if args.standard_io:
        USE_STANDARD_IO = True

    if not USE_STANDARD_IO and len(SERVER_SOCKETS) == 0 and len(SERIAL_DEVICES) == 0 and len(OPENED_FILES) == 0:
        exit(2)

    # create serving threads
    serving_threads = list()

    for serial_device in SERIAL_DEVICES:
        thread = Thread(target=client_handler, args=(serial_device, serial_device))
        thread.start()
        serving_threads.append(thread)

    for opened_file in OPENED_FILES:
        thread = Thread(target=client_handler, args=(opened_file, opened_file))
        thread.start()
        serving_threads.append(thread)

    if USE_STANDARD_IO:
        thread = Thread(target=client_handler, args=(sys.stdin, sys.stdout))
        thread.start()
        serving_threads.append(thread)

    # listen for incoming connections
    while not FLAG_SHUTDOWN:
        try:
            ready_socks = select.select(SERVER_SOCKETS, list(), list(), SELECT_TIMEOUT)[0]
        except select.error as e:
            if e[0] == 4:       # check interrupted system call
                break

        for sock in ready_socks:
            client_sock, client_addr = sock.accept()
            logging.info('client %s:%d connected', *client_addr)

            thread = Thread(target=client_handler, args=(client_sock, client_sock))
            thread.start()
            serving_threads.append(thread)

    for thread in serving_threads:
        thread.join()

if __name__ == '__main__':
    main()
