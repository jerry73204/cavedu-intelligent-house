import os.path
import pickle
import time
import tempfile
from threading import Thread

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
    midy = y + h // 2
    y1 = max(0, midy - crop_height // 2)
    y2 = min(image.shape[0] - 1, midy + crop_height // 2)
    return image[y1:y2, x:(x + w)]

def resize_image(image):
    return cv2.resize(image, (config.FACE_WIDTH, config.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)

def flip_image(image):
    return cv2.flip(image, 1)

class FaceAuthServie:
    def __init__(self, face_models_path, gui_service):
        self.gui_service = gui_service
        self.auth_thread = None
        self.flag_shutdown = False
        self.flag_train_request = False
        self.flag_recognition_request = False
        self.is_busy = False
        self.future_recognize_result = None
        self.camera = cv2.VideoCapture(0)

        self.face_models_path = face_models_path

        if os.path.isfile(face_models_path):
            with open(face_models_path, 'rb') as file_models:
                self.model_descriptions = pickle.load(file_models)
                assert isinstance(self.model_descriptions, list)

        else:
            self.model_descriptions = list()

    def create_face_identity(self):
        image_count = 0
        time_limit = time.time() + config.TRAINING_TASK_TIMEOUT
        training_images = list()

        # start training task
        while image_count < config.NUM_SAMPLED_TRAINING_IMAGES and time.time() < time_limit:
            progress_text = 'training... %d %%' % (image_count * 100 // config.NUM_SAMPLED_TRAINING_IMAGES)
            _, orig_image = self.camera.read()

            # get coordinates of single face in captured image
            gray_image = cv2.cvtColor(orig_image, cv2.COLOR_RGB2GRAY)
            result = detect_single_face(gray_image)

            # show captured image
            if result is None:
                orig_image = flip_image(orig_image)
                cv2.putText(orig_image, progress_text, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 240, 240), 1, 8)
                cv2.putText(orig_image, 'no face detected', (10, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1, 8)
                self.gui_service.camera_image = orig_image
                continue

            x, y, w, h = result
            cv2.rectangle(orig_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            orig_image = flip_image(orig_image)
            cv2.putText(orig_image, progress_text, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 240, 240), 1, 8)
            self.gui_service.camera_image = orig_image

            cropped_image = resize_image(crop_image(gray_image, x, y, w, h))
            training_images.append(cropped_image)

            image_count += 1

        # return None if timeout
        if image_count == 0:
            return None

        # train model
        labels = [POSITIVE_LABEL] * len(training_images) # create the label array
        model = cv2.face.createEigenFaceRecognizer()
        model.train(numpy.asarray(training_images), numpy.asarray(labels))

        # obtain the result
        with tempfile.NamedTemporaryFile() as tmp_file:
            model.save(tmp_file.name)
            model_description = tmp_file.read()

        return model_description

    def recognize_face(self, model_descriptions):
        # create face recognizers
        trained_models = list()

        for description in model_descriptions:
            with tempfile.NamedTemporaryFile() as tmp_file:
                tmp_file.file.write(description)
                tmp_file.flush()

                model = cv2.face.createEigenFaceRecognizer()
                model.load(tmp_file.name)
                trained_models.append(model)

        # start face recognition task
        face_count = 0
        time_limit = time.time() + config.RECOGNITION_TASK_TIMEOUT

        while face_count < config.NUM_SAMPLED_TESTING_IMAGES and time.time() < time_limit:
            # try to recognize a face
            _, orig_image = self.camera.read()
            gray_image = cv2.cvtColor(orig_image, cv2.COLOR_RGB2GRAY)
            result = detect_single_face(gray_image)

            # show captured image to screen
            if result is None:
                orig_image = flip_image(orig_image)
                cv2.putText(orig_image, 'Recognizing...', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 240, 240), 1, 8)
                self.gui_service.camera_image = orig_image
                continue

            x, y, w, h = result
            cv2.rectangle(orig_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            orig_image = flip_image(orig_image)
            cv2.putText(orig_image, 'Recognizing...', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 240, 240), 1, 8)
            self.gui_service.camera_image = orig_image

            # calculate confidence and vote
            face_count += 1
            cropped_image = resize_image(crop_image(gray_image, x, y, w, h))

            for model in trained_models:
                # label, confidence = model.predict(cropped_image)
                predict_collector = cv2.face.MinDistancePredictCollector()
                model.predict(cropped_image, predict_collector)
                label, confidence = predict_collector.getLabel(), predict_collector.getDist()

                if label == POSITIVE_LABEL and confidence < config.CONFIDENCE_THRESHOLD:
                    return True

        return False

    def worker(self):
        while True:
            if self.flag_shutdown:
                with open(self.face_models_path, 'wb') as file_models:
                    pickle.dump(self.model_descriptions, file_models)
                return

            elif self.flag_train_request:
                self.is_busy = True
                self.gui_service.flag_train_face = True

                description = self.create_face_identity()
                if description is not None:
                    self.model_descriptions.append(description)

                self.flag_train_request = False
                self.gui_service.flag_train_face = False
                self.is_busy = False

            elif self.flag_recognition_request:
                self.is_busy = True
                self.gui_service.flag_recognize_face = True

                result = self.recognize_face(self.model_descriptions)
                self.future_recognize_result.set_result(result)

                self.flag_recognition_request = False
                self.gui_service.flag_recognize_face = False
                self.is_busy = False

            else:
                _, frame = self.camera.read()
                frame = flip_image(frame)
                self.gui_service.camera_image = frame

    def start(self):
        self.auth_thread = Thread(target=self.worker)
        self.auth_thread.start()

    def stop(self):
        self.flag_shutdown = True
        self.auth_thread.join()

    def schedule_train_face(self):
        if not self.is_busy:
            self.flag_train_request = True
            return True
        else:
            return False

    def schedule_recognize_face(self, future):
        if not self.is_busy:
            self.future_recognize_result = future
            self.flag_recognition_request = True
            return True
        else:
            return False
