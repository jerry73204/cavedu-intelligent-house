#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time
import tempfile
import numpy
import cv2
import config

POSITIVE_LABEL = 1
HAAR_FACES = cv2.CascadeClassifier(config.HAAR_FACES)

def detect_single_face(image):
    faces = HAAR_FACES.detectMultiScale(image,
                                        scaleFactor=config.HAAR_SCALE_FACTOR,
                                        minNeighbors=config.HAAR_MIN_NEIGHBORS,
                                        minSize=config.HAAR_MIN_SIZE,
                                        flags=cv2.CASCADE_SCALE_IMAGE)
    if len(faces) != 1:
        return None

    return faces[0]

def crop_image(image, x, y, w, h):
    crop_height = int((config.FACE_HEIGHT / float(config.FACE_WIDTH)) * w)
    midy = y + h / 2
    y1 = max(0, midy-crop_height / 2)
    y2 = min(image.shape[0] - 1, midy + crop_height / 2)
    return image[y1:y2, x:(x + w)]

def resize_image(image):
    return cv2.resize(image, (config.FACE_WIDTH, config.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)

def create_face_identity(camera):
    image_count = 0
    time_limit = time.time() + config.TRAINING_TASK_TIMEOUT
    enable_training_time = time.time() + 1
    training_images = list()

    # start training task
    while image_count < config.NUM_SAMPLED_TRAINING_IMAGES and time.time() < time_limit:
        progress_text = 'training... %d %%' % (image_count * 100 / config.NUM_SAMPLED_TRAINING_IMAGES)
        _, orig_image = camera.read()

        # get coordinates of single face in captured image
        gray_image = cv2.cvtColor(orig_image, cv2.COLOR_RGB2GRAY)
        result = detect_single_face(gray_image)

        # show captured image
        if result is None:
            cv2.putText(orig_image, progress_text, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 240, 240), 1, 8)
            cv2.putText(orig_image, 'no face detected', (10, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1, 8)
            cv2.imshow('', orig_image)
            cv2.waitKey(config.FRAME_DELAY)
            enable_training_time = time.time() + 1
            continue

        else:
            x, y, w, h = result
            cv2.rectangle(orig_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(orig_image, progress_text, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 240, 240), 1, 8)
            cv2.imshow('', orig_image)
            cv2.waitKey(config.FRAME_DELAY)

        # skip the loop if the time is not ready
        if time.time() < enable_training_time:
            continue

        cropped_image = resize_image(crop_image(gray_image, x, y, w, h))
        training_images.append(cropped_image)

        image_count += 1
        enable_training_time = time.time() + 1

    # return None if timeout
    if image_count == 0:
        return None

    # train model
    labels = [POSITIVE_LABEL] * len(training_images) # create the label array
    model = cv2.createEigenFaceRecognizer()
    model.train(numpy.asarray(training_images), numpy.asarray(labels))

    # obtain the result
    with tempfile.NamedTemporaryFile() as tmp_file:
        model.save(tmp_file.name)
        model_description = tmp_file.read()

    return model_description

def recognize_face(camera, model_descriptions):
    # create face recognizers
    trained_models = list()

    for description in model_descriptions:
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.file.write(description)
            tmp_file.flush()

            model = cv2.createEigenFaceRecognizer()
            model.load(tmp_file.name)
            trained_models.append(model)

    # start face recognition task
    face_count = 0
    enable_recognitoin_time = time.time() + 1
    time_limit = time.time() + config.RECOGNITION_TASK_TIMEOUT

    while face_count < config.NUM_SAMPLED_TESTING_IMAGES and time.time() < time_limit:
        # try to recognize a face
        _, orig_image = camera.read()
        gray_image = cv2.cvtColor(orig_image, cv2.COLOR_RGB2GRAY)
        result = detect_single_face(gray_image)

        # show captured image to screen
        if result is None:
            cv2.putText(orig_image, 'Recognizing...', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 240, 240), 1, 8)
            cv2.imshow('', orig_image)
            cv2.waitKey(config.FRAME_DELAY)
            continue

        else:
            x, y, w, h = result
            cv2.rectangle(orig_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(orig_image, 'Recognizing...', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 240, 240), 1, 8)
            cv2.imshow('', orig_image)
            cv2.waitKey(config.FRAME_DELAY)

        # skip the loop if the time is not ready
        if time.time() < enable_recognitoin_time:
            continue

        # calculate confidence and vote
        face_count += 1
        cropped_image = resize_image(crop_image(gray_image, x, y, w, h))

        for index, model in enumerate(trained_models):
            label, confidence = model.predict(cropped_image)

            if label == POSITIVE_LABEL and confidence < config.CONFIDENCE_THRESHOLD:
		return True

    return False
