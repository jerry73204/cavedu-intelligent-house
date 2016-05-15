# Copyright (C) HENNES CO., LTD. - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written in May 2016 by
# Li-Wei Shih
# Hao-Yun Hsueh
# Feng-Chih Hsu
# Hsiang-Jiu Lin
# Cheng-Chang Liu
# Pei-Hsuan Yan
import os

# GPIO
PIN_OUT_INVADED      = 21
PIN_OUT_TIMEOUT      = 20
PIN_OUT_LOCK         = 11
PIN_OUT_LIGHT        = 9
PIN_IN_EMERGENCY     = 16
PIN_IN_MAGNET_SWITCH = 22

# serial
SERIAL_DEVICE_PATH   = '/dev/ttyAMA0'
SERIAL_BAUDRATE = 9600

# MediaTek cloud
DEVICE_ID = 'DGDfnSwk'
DEVICE_KEY = 'SHKVwfd9mma1YisF'
CHANNEL_STATUS_ID = 'house_status'

# GUI
WEBCAM_IMAGE_WIDTH  = 400
WEBCAM_IMAGE_HEIGHT = 300

# face recognition
FACES_DATABASE_PATH = './faces.db'

FRAME_DELAY = 20

TRAINING_TASK_TIMEOUT = 10
RECOGNITION_TASK_TIMEOUT = 10

CONFIDENCE_THRESHOLD = 1100
SUCCESS_RATE_THRESHOLD = 0.7

NUM_SAMPLED_TRAINING_IMAGES = 5
NUM_SAMPLED_TESTING_IMAGES  = 3

HAAR_FACES         =  '%s/haarcascade_frontalface_alt.xml' % os.path.dirname(os.path.realpath(__file__))
HAAR_SCALE_FACTOR  = 1.3
HAAR_MIN_NEIGHBORS = 4
HAAR_MIN_SIZE      = (30, 30)

FACE_WIDTH  = 92
FACE_HEIGHT = 112
