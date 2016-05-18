#!/usr/bin/env python2
import re
import sys
import argparse
import socket
import select
from threading import Thread

import serial

SERVER_SOCKETS = list()
SERIAL_DEVICES = list()
OPENED_FILES = list()
USE_STANDARD_IO = False

def client_handler(reader, writer):
    pass

def main():
    global USE_STANDARD_IO

    # argument specification
    arg_parser = argparse.ArgumentParser(description='CAVEDU intelligent house client')
    arg_parser.add_argument('--device',
                            required=True,
                            metavar='DEVICE_TYPE',
                            choices=['MT7688', 'Pi1', 'Pi2', 'Pi3'],
                            nargs=1,
                            help='specify the device model. DEVICE_TYPE can be either MT7688, Pi1, Pi2, Pi3')
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

    if args.network is not None:
        for arg in args.network:
            _, host, port = re.findall('^(([^:]+):)?(\d{1,5})$', arg[0])[0]
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
    while True:
        # TODO timeout
        ready_socks = select.select(SERVER_SOCKETS, list(), list())[0]

        for sock in ready_socks:
            client_sock, _ = sock.accept()
            thread = Thread(target=client_handler, args=(client_sock, client_sock))
            thread.start()
            serving_threads.append(thread)

if __name__ == '__main__':
    main()
