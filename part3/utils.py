#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import time
import shutil
import fnmatch
import numpy
import cv2

TRAINING_FILE = 'training.xml'

POSITIVE_LABEL = 1
NEGATIVE_LABEL = 2

MEAN_FILE = 'mean.png'
POSITIVE_EIGENFACE_FILE = 'positive_eigenface.png'
NEGATIVE_EIGENFACE_FILE = 'negative_eigenface.png'

POSITIVE_DIR = './training/positive'
NEGATIVE_DIR = './training/negative'

HAAR_FACES         = 'haarcascade_frontalface_alt.xml'
HAAR_SCALE_FACTOR  = 1.3
HAAR_MIN_NEIGHBORS = 4
HAAR_MIN_SIZE      = (30, 30)

FACE_WIDTH  = 92
FACE_HEIGHT = 112

NUM_TRAINING_IMAGES = 10

# Prefix for positive training image filenames.
POSITIVE_FILE_PREFIX = 'positive_'

haar_faces = cv2.CascadeClassifier(HAAR_FACES)

def walk_files(directory, match='*'):
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, match):
            yield os.path.join(root, filename)

def prepare_image(filename):
    return resize(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

def normalize(X, low, high, dtype=None):
    X = numpy.asarray(X)
    minX, maxX = numpy.min(X), numpy.max(X)
    # normalize to [0...1].
    X = X - float(minX)
    X = X / float((maxX - minX))
    # scale to [low...high].
    X = X * (high-low)
    X = X + low
    if dtype is None:
        return numpy.asarray(X)
    return numpy.asarray(X, dtype=dtype)

def detect_single(image):
    faces = haar_faces.detectMultiScale(image,
                                        scaleFactor=HAAR_SCALE_FACTOR,
                                        minNeighbors=HAAR_MIN_NEIGHBORS,
                                        minSize=HAAR_MIN_SIZE,
                                        flags=cv2.CASCADE_SCALE_IMAGE)
    if len(faces) != 1:
        return None

    return faces[0]

def crop_image(image, x, y, w, h):
    crop_height = int((FACE_HEIGHT / float(FACE_WIDTH)) * w)
    midy = y + h / 2
    y1 = max(0, midy-crop_height / 2)
    y2 = min(image.shape[0] - 1, midy + crop_height / 2)
    return image[y1:y2, x:(x + w)]

def resize(image):
    return cv2.resize(image, (FACE_WIDTH, FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)

def capture_positives(camera):
    # delete all faces
    if os.path.exists(POSITIVE_DIR):
        shutil.rmtree(POSITIVE_DIR)

    os.makedirs(POSITIVE_DIR)

    count = 0
    working_time = 0

    while True:
        # capture image
        progress_text = 'training... %d %%' % (count * 100 / NUM_TRAINING_IMAGES)

        _, orig_image = camera.read()

        # get coordinates of single face in captured image
        gray_image = cv2.cvtColor(orig_image, cv2.COLOR_RGB2GRAY)
        result = detect_single(gray_image)

        if result is None:
            cv2.putText(orig_image, progress_text, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 240, 240), 1, 8)
            cv2.putText(orig_image, 'no face detected', (10, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1, 8)
            cv2.imshow('', orig_image)
            cv2.waitKey(1)
            continue

        else:
            # show face location in screen
            x, y, w, h = result
            cv2.rectangle(orig_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(orig_image, progress_text, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 240, 240), 1, 8)
            cv2.imshow('', orig_image)
            cv2.waitKey(1)

        # skip if
        if time.time() < working_time:
            continue

        # Save image to file.
        cropped_image = crop_image(gray_image, x, y, w, h)
        filename = os.path.join(POSITIVE_DIR, POSITIVE_FILE_PREFIX + '%03d.pgm' % count)

        cv2.imwrite(filename, cropped_image)

        count += 1
        if count == NUM_TRAINING_IMAGES:
            break

        working_time = time.time() + 1

def train():
    faces = []
    labels = []
    pos_count = 0
    neg_count = 0

    # Read all positive images
    for filename in walk_files(POSITIVE_DIR, '*.pgm'):
        faces.append(prepare_image(filename))
        labels.append(POSITIVE_LABEL)
        pos_count += 1

    # Read all negative images
    for filename in walk_files(NEGATIVE_DIR, '*.pgm'):
        faces.append(prepare_image(filename))
        labels.append(NEGATIVE_LABEL)
        neg_count += 1

    # print 'Read', pos_count, 'positive images and', neg_count, 'negative images.'

    # Train model
    # print 'Training model...'
    model = cv2.createEigenFaceRecognizer()
    model.train(numpy.asarray(faces), numpy.asarray(labels))

    # Save model results
    model.save(TRAINING_FILE)
    # print 'Training data saved to', TRAINING_FILE

    # Save mean and eignface images which summarize the face recognition model.
    mean = model.getMat('mean').reshape(faces[0].shape)
    cv2.imwrite(MEAN_FILE, normalize(mean, 0, 255, dtype=numpy.uint8))

    eigenvectors = model.getMat("eigenvectors")
    pos_eigenvector = eigenvectors[:,0].reshape(faces[0].shape)
    cv2.imwrite(POSITIVE_EIGENFACE_FILE, normalize(pos_eigenvector, 0, 255, dtype=numpy.uint8))

    neg_eigenvector = eigenvectors[:,1].reshape(faces[0].shape)
    cv2.imwrite(NEGATIVE_EIGENFACE_FILE, normalize(neg_eigenvector, 0, 255, dtype=numpy.uint8))
