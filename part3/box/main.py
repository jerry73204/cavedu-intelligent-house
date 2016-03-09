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
		elif global_flag_start_recognition == 1:
			private_success = 0
			face_count = 0
			global_flag_start_recognition = 0
			model = cv2.createEigenFaceRecognizer()
			model.load(config.TRAINING_FILE)
			start_time = time.time()
			while face_count < 5 and time.time()-start_time < 5:
				ret, image = camera.read()
				image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
				result = face.detect_single(image)
				if result is None:
						print 'Could not detect single face!  Check the image in capture.pgm' \
							  ' to see what was captured and try again with only one face visible.'
						continue
				face_count = face_count + 1
				x, y, w, h = result
				# Crop and resize image to face.
				crop = face.resize(face.crop(image, x, y, w, h))
				# Test face against model.
				label, confidence = model.predict(crop)
				print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
					'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', 
					confidence)
				if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
					print 'Recognized face!'
					private_success = 1
					break
				else:
					print 'Did not recognize face!'
			if private_success == 1:
				global_flag_recognition_success = 1
			global_flag_recognition_finished = 1
		else:
			cv2.waitKey(30)
		

