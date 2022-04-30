import face_recognition
import numpy as np
from PIL import Image, ImageDraw
import os
import io
import base64


class FaceRec:
    # def __init__(self, known_person_path_file, unknown_images_path_file, known_name=None):
    #     self.known_person_path_file = known_person_path_file
    #     self.unknown_images_path_file = unknown_images_path_file
    #     self.known_name = known_name

    def __init__(self):
        self.unknown_images_path_file = 'stranger'
        self.known_names = []
        self.known_encodings = []
        dirname = 'known-people'
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_encodings.append(face_encoding)
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def converted_known_image(self):
        return face_recognition.load_image_file('known-people')
        # return face_recognition.load_image_file(self.known_person_path_file)

    def recognize_faces(self):
        for file in os.listdir(self.unknown_images_path_file):
            if file[0] != '.':
                # known_image = self.converted_known_image()
                # known_image_encoding = face_recognition.face_encodings(known_image)[0]
                known_face_encodings = self.known_encodings
                known_face_names = self.known_names

                unknown_image = face_recognition.load_image_file(self.unknown_images_path_file + '/' + file)

                ##
                face_locations = face_recognition.face_locations(unknown_image)
                face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
                self.face_names = []
                for face_encoding in face_encodings:
                    distances = face_recognition.face_distance(self.known_encodings, face_encoding)
                    min_value = min(distances)
                    name = 'unknown'
                    if min_value < 0.6:
                        index = np.argmin(distances)
                        name = self.known_names[index]
                    self.face_names.append(name)
                print(self.known_names)
                print(self.face_names)

                ####
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "unknown"

                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        return name

                    return name


faces = FaceRec()
