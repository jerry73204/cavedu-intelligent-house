#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import logging
import signal

# import RPi.GPIO as GPIO
import tornado.web
import tornado.ioloop

import config
import constants
import __version__

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

        data = tornado.escape.json_decode(self.request.body)

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
            # GPIO.setup(pin, GPIO.OUT)

        # update GPIO output pins
        GPIO_OUTPUT_PINS = gpio_output_pins

        # update GPIO input pins
        for removed_pins in GPIO_INPUT_PINS_WITH_SAVED_VALUES.keys - gpio_input_pins:
            del GPIO_INPUT_PINS_WITH_SAVED_VALUES[removed_pins]

        for inserted_pins in gpio_input_pins - GPIO_INPUT_PINS_WITH_SAVED_VALUES.keys():
            GPIO_INPUT_PINS_WITH_SAVED_VALUES[inserted_pins] = None

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
    def get(self, device_path, read_size):
        def error_response(reason):
            response = {
                'status': 'error',
                'reason': reason
            }
            self.write(response)

        read_size = int(read_size)
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
    def get(self, device_path):
        def error_response(reason):
            response = {
                'status': 'error',
                'reason': reason
            }
            self.write(response)

        if device_path not in SERIAL_DEVICES:
            error_response('"%s" is not a valid serial device')
            return

        data = self.request.body

        serial_object = SERIAL_DEVICES[device_path]
        serial_object.write(data)

        response = {
            'status': 'ok',
        }
        self.write(response)

def house_periodic_worker():
    global GPIO_INPUT_PINS_WITH_SAVED_VALUES

    for pin, saved_value in enumerate(GPIO_INPUT_PINS_WITH_SAVED_VALUES):
        curr_value = 0
        # curr_value = GPIO.input(pin)
        GPIO_INPUT_PINS_WITH_SAVED_VALUES[pin] = curr_value

        if saved_value is not None and saved_value != curr_value:
            # TODO trigger change event
            pass

    for device_path, serial_object in SERIAL_DEVICES:
        if serial_object.in_waitint() > 0:
            # TODO trigger serial eventx
            pass

def signal_handler(signum, frame):
    # constants.SHUTDOWN_FLAG = True
    tornado.ioloop.IOLoop.current().stop()

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    signal.signal(signal.SIGINT, signal_handler)
    tornado.log.enable_pretty_logging()

    app = tornado.web.Application([
        (r"/info", InfoHandler),
        (r"/update-config", UpdateConfigHandler),
        (r"/gpio/read/(\d+)", GpioReadHandler),
        (r"/gpio/write/(\d+)/(0|1)", GpioWriteHandler),
    ])
    app.listen(config.LISTEN_PORT)

    tornado.ioloop.PeriodicCallback(house_periodic_worker, 10).start()
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
