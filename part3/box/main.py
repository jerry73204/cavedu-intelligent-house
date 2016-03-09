import cv2
import train
import capture_positives
import time

global_flag_start_training = 0
global_flag_training_finished = 0
global_flag_start_recognition = 0
global_flag_recognition_finished = 0
global_flag_recognition_success = 0

if __name__ == '__main__':
	camera = cv2.VideoCapture(0)
	while True:
		ret,frame = camera.read()
		cv2.imshow('aaa',frame)
		if global_flag_start_training == 1:
			global_flag_start_training = 0
			capture_positives.capture_positives(camera)
			train.train()
			global_flag_training_finished = 1
			
		else:
			cv2.waitKey(30)
		

