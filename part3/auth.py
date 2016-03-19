#!/usr/bin/env python2

import cv2
import utils
import time

FLAG_START_TRAINING       = False
FLAG_TRAINING_FINISHED    = False
FLAG_START_RECOGNITION    = False
FLAG_RECOGNITION_FINISHED = False
FLAG_RECOGNITION_SUCCESS  = False
FLAG_SHUTDOWN             = False

def auth_worker():
    global FLAG_START_TRAINING
    global FLAG_TRAINING_FINISHED
    global FLAG_START_RECOGNITION
    global FLAG_RECOGNITION_FINISHED
    global FLAG_RECOGNITION_SUCCESS

    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        cv2.imshow('', frame)
        cv2.waitKey(1)

        if FLAG_SHUTDOWN:
            return

        elif FLAG_START_TRAINING:
            utils.capture_positives(camera)
            utils.train()
            FLAG_START_TRAINING, FLAG_TRAINING_FINISHED = False, True

        elif FLAG_START_RECOGNITION:
            face_count = 0
            FLAG_START_RECOGNITION = False
            model = cv2.createEigenFaceRecognizer()
            model.load(config.TRAINING_FILE)
            start_time = time.time()

            while face_count < 5 and time.time()-start_time < 20:
                ret, image0 = camera.read()
                cv2.imshow('', image0)
                cv2.waitKey(1)
                image = cv2.cvtColor(image0, cv2.COLOR_RGB2GRAY)
                result = face.detect_single(image)

                if result is None:
                    print 'Could not detect single face!  Check the image in capture.pgm' + \
                        ' to see what was captured and try again with only one face visible.'
                    continue

                face_count += 1
                x, y, w, h = result
                cv2.rectangle(image0, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow('', image0)
                cv2.waitKey(1)
                time.sleep(1)

                start_time = start_time + 1
                # Crop and resize image to face.
                crop = face.resize(face.crop(image, x, y, w, h))
                # Test face against model.
                label, confidence = model.predict(crop)

                print 'Predicted %s face with confidence %d (lower is more confident).' % \
                    ('POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', confidence)

                if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
                    print 'Recognized face!'
                    FLAG_RECOGNITION_SUCCESS = True
                    break

                else:
                    print 'Did not recognize face!'

            FLAG_RECOGNITION_FINISHED = True
        else:
            cv2.waitKey(30)
