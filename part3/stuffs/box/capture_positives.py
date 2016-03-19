"""Raspberry Pi Face Recognition Treasure Box
Positive Image Capture Script
Copyright 2013 Tony DiCola 

Run this script to capture positive images for training the face recognizer.
"""
import glob
import os
import sys
import select

import cv2

import config
import face
import time
import shutil


# Prefix for positive training image filenames.
POSITIVE_FILE_PREFIX = 'positive_'

def capture_positives(camera):
	'''
	# Create the directory for positive training images if it doesn't exist.
	if not os.path.exists(config.POSITIVE_DIR):
		os.makedirs(config.POSITIVE_DIR)
	# Find the largest ID of existing positive images.
	# Start new images after this ID value.
	files = sorted(glob.glob(os.path.join(config.POSITIVE_DIR, 
		POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
	if len(files) > 0:
		# Grab the count from the last filename.
		count = int(files[-1][-7:-4])+1
	'''
	#Delete all faces
	if os.path.exists(config.POSITIVE_DIR):
		shutil.rmtree(config.POSITIVE_DIR)
	count = 0
	while True:
		print 'Capturing image...'
		ret, image0 = camera.read()
		cv2.imshow('aaa',image0)
		cv2.waitKey(1)
		# Convert image to grayscale.
		image = cv2.cvtColor(image0, cv2.COLOR_RGB2GRAY)
		# Get coordinates of single face in captured image.
		result = face.detect_single(image)
		if result is None:
			print 'Could not detect single face!  Check the image in capture.pgm' \
				  ' to see what was captured and try again with only one face visible.'
			continue
		x, y, w, h = result
		# Crop image as close as possible to desired face aspect ratio.
		# Might be smaller if face is near edge of image.
		crop = face.crop(image, x, y, w, h)
		# Rect the face on screen
		cv2.rectangle(image0,(x,y),(x+w,y+h),(0,255,0),2)
		cv2.imshow('aaa',image0)
		cv2.waitKey(1)
		# Save image to file.
		filename = os.path.join(config.POSITIVE_DIR, POSITIVE_FILE_PREFIX + '%03d.pgm' % count)
		cv2.imwrite(filename, crop)
		print 'Found face and wrote training image', filename
		count += 1
		if count == 10:
			break
		time.sleep(1)
