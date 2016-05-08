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

class InfoHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class UpdateConfigHandler(tornado.web.RequestHandler):
    def get(self):
        # TODO
        pass

class GpioReadHandler(tornado.web.RequestHandler):
    def get(self, pin_number):
        pin_number = int(pin_number)

        if pin_number in constants.GPIO_PIN_NUMBERS:
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

        if pin_number in constants.GPIO_PIN_NUMBERS:
            # GPIO.output(pin_number, value)

            response = {
                'status': 'ok',
            }

        else:
            response = {
                'status': 'error',
                'reason': '%d is not a valid GPIO pin number' % pin_number
            }

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
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
