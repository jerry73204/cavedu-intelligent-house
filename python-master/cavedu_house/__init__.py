import os
import json
import socket
import serial

CHANNEL_TYPE_NETWORK = 0
CHANNEL_TYPE_SERIAL  = 1
CHANNEL_TYPE_FILE    = 2

class HouseDevice:
    def __init__(self, channel_type, **kargs):
        assert channel_type in (CHANNEL_TYPE_NETWORK, CHANNEL_TYPE_SERIAL, CHANNEL_TYPE_FILE)

        self.channel_type = channel_type

        if channel_type == CHANNEL_TYPE_NETWORK:
            address = kargs['address']
            port = kargs['port']
            connect_network(address, port)

        elif channel_type == CHANNEL_TYPE_SERIAL:
            device = kargs['device']
            baudrate = kargs['baudrate']
            connect_serial(device, baudrate)

        elif channel_type == CHANNEL_TYPE_FILE:
            input_path = kargs['input_file']
            output_path = kargs['output_file']
            connect_file(input_path, output_path)

    def connect_network(self, address, port):
        self.address = address
        self.port = port

        sock = socket.create_connection((address, port))
        self.reader = sock
        self.writer = sock

    def connect_serial(self, device, baudrate):
        self.device = device
        self.baudrate = baudrate

        serial_device = serial.Serial(serial_path, baudrate=baudrate)
        self.reader = serial_device
        self.writer = serial_device

    def connect_file(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

        self.reader = open(input_path, 'rb')
        self.writer = open(input_path, 'wb')

    def try_reconnect(self):
        # TODO handle exception and retry

        if channel_type == CHANNEL_TYPE_NETWORK:
            connect_network(self.address, self.port)

        elif channel_type == CHANNEL_TYPE_SERIAL:
            connect_serial(self.device, self.baudrate)

        elif channel_type == CHANNEL_TYPE_FILE:
            connect_file(self.input_path, self.output_path)

    def close():
        self.reader.close()
        self.writer.close()

    def send_request(request):
        request_buffer = json.dumps(request)
        request_buffer = struct.pack('<I', len(request_buffer)) + request_buffer

        # send request
        size_left = len(request_buffer)

        while size_left > 0:
            size_written = os.write(self.writer.fileno(), request_payload)
            size_left -= size_written
            request_buffer = request_buffer[size_written:]

        # receive response size
        size_buffer = ''
        size_left = 4

        while size_left > 0:
            payload = os.read(self.reader.fileno(), size_left)

            if len(payload) == 0: # check if file is closed or reaches EOF
                # TODO check error
                try_reconnect()

            size_left -= len(payload)
            size_buffer += payload

        # receive response
        size_left = struct.unpack('<I', size_buffer)[0]
        response_buffer = ''

        while size_left > 0:
            payload = os.read(self.reader.fileno(), size_left)

            if len(payload) == 0: # check if file is closed or reaches EOF
                # TODO check error
                try_reconnect()

            size_left -= len(payload)
            response_buffer += payload

        return json.loads(response_buffer)

    def gpio_read(self, pin):
        pass

    def gpio_write(self, pin, value):
        pass

    def i2c_read(self, register):
        pass

    def i2c_write(self, register, value):
        pass

    def serial_read(self):
        pass

    def serial_write(self, payload):
        pass
