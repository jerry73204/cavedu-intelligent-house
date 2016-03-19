import time
import cv2
import utils

FLAG_BUSY                = False
FLAG_SHUTDOWN            = False
FLAG_TRAIN_REQUEST       = False
FLAG_RECOGNITION_REQUEST = False
FLAG_RECOGNITION_RESULT  = False
LAST_RECOGNITION_TIME    = 0

def auth_worker():
    global FLAG_BUSY
    global FLAG_SHUTDOWN
    global FLAG_TRAIN_REQUEST
    global FLAG_RECOGNITION_REQUEST
    global FLAG_RECOGNITION_RESULT
    global LAST_RECOGNITION_TIME

    model_descriptions = list()
    camera = cv2.VideoCapture(0)

    while True:
        if FLAG_SHUTDOWN:
            return

        elif FLAG_TRAIN_REQUEST:
            FLAG_BUSY = True
            FLAG_TRAIN_REQUEST = False
            FLAG_RECOGNITION_RESULT = False

            description = utils.create_face_identity(camera)
            model_descriptions.append(description)

            FLAG_BUSY = False

        elif FLAG_RECOGNITION_REQUEST:
            FLAG_BUSY = True
            FLAG_RECOGNITION_REQUEST = False
            FLAG_RECOGNITION_RESULT = False

            result = utils.recognize_face(camera, model_descriptions)
            FLAG_RECOGNITION_RESULT = result
            LAST_RECOGNITION_TIME = time.time()

            FLAG_BUSY = False

        else:                   # idle state
            _, frame = camera.read()
            cv2.imshow('', frame)
            cv2.waitKey(1)
