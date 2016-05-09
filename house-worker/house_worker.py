#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import logging
import signal

# import RPi.GPIO as GPIO
import serial
import tornado.web
import tornado.ioloop
import tornado.httpclient

import config
import constants
import __version__

MASTER_ADDRESS = None
MASTER_PORT = None
GPIO_INPUT_PINS_WITH_SAVED_VALUES = dict()
GPIO_OUTPUT_PINS = set()
SERIAL_DEVICES = dict()

class InfoHandler(tornado.web.RequestHandler):
    def get(self):
        info = {
            'version': __version__.VERSION
        }
        self.write(info)

class UpdateConfigHandler(tornado.web.RequestHandler):
    def get(self):
        def error_response(reason):
            response = {
                'status': 'error',
                'reason': reason
            }
            self.write(response)

        global GPIO_INPUT_PINS_WITH_SAVED_VALUES
        global GPIO_OUTPUT_PINS
        global SERIAL_DEVICES

        data = tornado.escape.json_decode(self.request.body)

        # verify GPIO configuration
        gpio_input_pins = set(data['gpio']['inputs'])
        gpio_output_pins = set(data['gpio']['outputs'])

        if len(gpio_input_pins & gpio_output_pins) != 0:
            error_response('no GPIO pins cannot be in both input and output modes')
            return

        for pin in gpio_input_pins:
            if pin not in constants.GPIO_PIN_NUMBERS:
                error_response('%d is not a valid GPIO pin number' % pin)
                return
            # GPIO.setup(pin, GPIO.IN)

        for pin in gpio_output_pins:
            if pin not in constants.GPIO_PIN_NUMBERS:
                error_response('%d is not a valid GPIO pin number' % pin)
                return

        # update GPIO output pins
        GPIO_OUTPUT_PINS = gpio_output_pins
        for pin in gpio_output_pins:
            # GPIO.setup(pin, GPIO.OUT)
            pass

        # update GPIO input pins
        for removed_pins in GPIO_INPUT_PINS_WITH_SAVED_VALUES.keys - gpio_input_pins:
            del GPIO_INPUT_PINS_WITH_SAVED_VALUES[removed_pins]

        for inserted_pins in gpio_input_pins - GPIO_INPUT_PINS_WITH_SAVED_VALUES.keys():
            GPIO_INPUT_PINS_WITH_SAVED_VALUES[inserted_pins] = None
            # GPIO.setup(pin, GPIO.IN)

        # update serial device configuration
        for device_path, serial_object in SERIAL_DEVICES:
            serial_object.close()
        SERIAL_DEVICES = dict()

        serial_devices = dict()
        for device_path, baudrate in data['serial']:
            if device_path in serial_devices:
                error_response('the serial device "%s" is specified more than once' % device_path)
                return

            try:
                serial_object = serial.Serial(port=device_path, baudrate=baudrate)
                serial_devices[device_path] = serial_object

            except serial.SerialException:
                for serial_obj in serial_devices.values():
                    serial_obj.close()

                error_response('failed to open serial port "%s"' % device_path)
                return

        SERIAL_DEVICES = serial_devices

class GpioReadHandler(tornado.web.RequestHandler):
    def get(self, pin_number):
        pin_number = int(pin_number)

        if pin_number in constants.GPIO_PIN_NUMBERS and pin_number in GPIO_INPUT_PINS_WITH_SAVED_VALUES:
            response = {
                'status': 'ok',
                'value': 123
                # 'value': GPIO.input(pin_number)
            }
        else:
            response = {
                'status': 'error',
                'reason': '%d is not a valid GPIO pin number' % pin_number
            }

        self.write(response)

class GpioWriteHandler(tornado.web.RequestHandler):
    def get(self, pin_number, value):
        pin_number = int(pin_number)
        value = int(value)

        if pin_number in constants.GPIO_PIN_NUMBERS and pin_number in GPIO_OUTPUT_PINS:
            # GPIO.output(pin_number, value)

            response = {
                'status': 'ok',
            }

        else:
            response = {
                'status': 'error',
                'reason': '%d is not a valid GPIO pin number' % pin_number
            }

        self.write(response)

class SerialReadHandler(tornado.web.RequestHandler):
    def get(self):
        def error_response(reason):
            response = {
                'status': 'error',
                'reason': reason
            }
            self.write(response)

        request_data = tornado.escape.json_decode(self.request.body)
        read_size = request_data['size']
        device_path = request_data['path']

        if read_size < 0:
            error_response('%d is not a valid buffer size' % read_size)
            return

        if device_path not in SERIAL_DEVICES:
            error_response('"%s" is not a valid serial device')
            return

        serial_object = SERIAL_DEVICES[device_path]
        payload = serial_object.read(read_size)

        response = {
            'status': 'ok',
            'data': payload
        }
        self.write(response)

class SerialWriteHandler(tornado.web.RequestHandler):
    def get(self):
        def error_response(reason):
            response = {
                'status': 'error',
                'reason': reason
            }
            self.write(response)

        request_data = tornado.escape.json_decode(self.request.body)
        device_path = request_data['path']
        payload = request_data['data']

        if device_path not in SERIAL_DEVICES:
            error_response('"%s" is not a valid serial device')
            return

        serial_object = SERIAL_DEVICES[device_path]
        serial_object.write(payload)

        response = {
            'status': 'ok',
        }
        self.write(response)

def trigger_event_on_master(event, data):
    url = 'http://%s:%d/api' % (MASTER_ADDRESS, MASTER_PORT)
    body = {
        'event': event,
        'data': data
    }

    request = tornado.httpclient.HTTPRequest(url, body=body)

    try:
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch(request)

    except tornado.httpclient.HTTPError:
        logging.error('cannot connect to address "http://%s:%d/api"',MASTER_ADDRESS, MASTER_PORT)

def house_periodic_worker():
    for pin, saved_value in enumerate(GPIO_INPUT_PINS_WITH_SAVED_VALUES):
        curr_value = 0
        # curr_value = GPIO.input(pin)
        GPIO_INPUT_PINS_WITH_SAVED_VALUES[pin] = curr_value

        if saved_value is not None and saved_value != curr_value:
            data = {
                'pin': pin,
                'from': saved_value,
                'to': curr_value
            }
            trigger_event_on_master('gpio_input_change', data)

    for device_path, serial_object in SERIAL_DEVICES:
        if serial_object.in_waitint() > 0:
            data = {
                'path': device_path
            }
            trigger_event_on_master('serial_has_input', data)

def signal_handler(signum, frame):
    # constants.SHUTDOWN_FLAG = True
    tornado.ioloop.IOLoop.current().stop()

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    signal.signal(signal.SIGINT, signal_handler)
    tornado.log.enable_pretty_logging()

    app = tornado.web.Application([
        (r'/info', InfoHandler),
        (r'/update-config', UpdateConfigHandler),
        (r'/gpio/read/(\d+)', GpioReadHandler),
        (r'/gpio/write/(\d+)/(0|1)', GpioWriteHandler),
        (r'/serial/read', SerialReadHandler),
        (r'/serial/write', SerialWriteHandler),
    ])
    app.listen(config.LISTEN_PORT)

    tornado.ioloop.PeriodicCallback(house_periodic_worker, 10).start()
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
