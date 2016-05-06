from threading import Thread

import serial

import config

class RfidService:
    def __init__(self):
        self.serial_rfid = serial.Serial(
            port=config.SERIAL_DEVICE_PATH,
            baudrate=config.SERIAL_BAUDRATE,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.5
        )
        self.rfid_thread = None
        self.flag_shutdown = False
        self.flag_tag_detected = False

    def worker(self):
        while True:
            if self.flag_shutdown:
                return

            payload = self.serial_rfid.read(14)
            if len(payload) != 0:
                self.flag_tag_detected = True

    def is_tag_detected(self):
        result = self.flag_tag_detected
        if result:
            self.flag_tag_detected = False
        return result

    def start(self):
        self.rfid_thread = Thread(target=self.worker)
        self.rfid_thread.start()

    def stop(self):
        self.flag_shutdown = True
        self.rfid_thread.join()
