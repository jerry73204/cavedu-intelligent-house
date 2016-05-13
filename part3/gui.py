# -*- coding: utf-8 -*-
import Tkinter as tk
from PIL import Image, ImageTk
from threading import Thread

import cv2

import config
import constants

class GuiServie:
    def __init__(self):
        self.auth_thread = None
        self.flag_shutdown = False
        self.signal_train_face = False
        self.signal_recognize_face = False
        self.state = constants.STATE_OPEN
        self.camera_image = None

    def get_camera_tk_image(self):
        if self.camera_image is not None:
            resized_image = cv2.resize(self.camera_image, (config.WEBCAM_IMAGE_WIDTH, config.WEBCAM_IMAGE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)
            return ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGBA)))
        else:
            return None

    def is_signaled_train_face(self):
        result = self.signal_train_face
        if result:
            self.signal_train_face = False

        return result

    def is_signaled_recognize_face(self):
        result = self.signal_recognize_face
        if result:
            self.signal_recognize_face = False

        return result

    def set_house_state(self, state):
        self.state = state

    def worker(self):
        tk_root = tk.Tk()
        tk_root.title('CAVEDU智慧屋')
        tk_root.bind('<Escape>', lambda e: tk_root.quit())

        tk_label_status = tk.Label(tk_root, font=('', 12), text='')
        tk_label_status.pack(fill='x')

        tk_label_image = tk.Label(tk_root)
        tk_label_image.pack()

        def command_train_face():
            self.signal_train_face = True

        def command_recognize_face():
            self.signal_recognize_face = True

        button_train_face = tk.Button(tk_root, text='記下特徵', font=('', 16), command=command_train_face)
        button_train_face.pack(side=tk.LEFT)

        button_recognize_face = tk.Button(tk_root, text='認證', font=('', 16), command=command_recognize_face)
        button_recognize_face.pack(side=tk.LEFT)

        def refresh():
            if self.flag_shutdown:
                tk_root.quit()
                return

            if self.state == constants.STATE_OPEN:
                tk_label_status.config(text='可進出', background='green yellow')

            elif self.state == constants.STATE_CLOSED:
                tk_label_status.config(text='禁止出入', background='yellow')

            elif self.state == constants.STATE_EMERGENCY:
                tk_label_status.config(text='緊急狀態', background='red')

            elif self.state == constants.STATE_INVADED:
                tk_label_status.config(text='遭遇入侵', background='red')

            else:
                assert False

            tk_image = self.get_camera_tk_image()

            if tk_image is not None:
                tk_label_image.imgtk = tk_image
                tk_label_image.configure(image=tk_image)

            tk_label_image.after(config.FRAME_DELAY, refresh)

        refresh()
        tk_root.mainloop()
        constants.SHUTDOWN_FLAG = True

    def start(self):
        self.auth_thread = Thread(target=self.worker)
        self.auth_thread.start()

    def stop(self):
        self.flag_shutdown = True
        self.auth_thread.join()
