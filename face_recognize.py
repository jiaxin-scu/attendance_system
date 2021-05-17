import os
import pickle
import cv2
import numpy as np
import utils
from inception import InceptionResNetV1
import mtcnn


class face_rec():
    """Face recognition of the main classes"""
    

    def __init__(self):
        """ initialization
            mtcnn_model：Used to extract face frame, output 5 key points (eyes, mouth, nose tip)  
            facenet_model：Face recognition model, output 128 individual face feature points
        """
        self.mtcnn_model = mtcnn.MTCNN()
        self.threshold = [0.5, 0.6, 0.8]
        self.facenet_model = InceptionResNetV1()
        model_path = 'model/facenet_keras.h5'
        self.facenet_model.load_weights(model_path)
        self.known_face_encodings = []
        self.known_face_names = []

        # Import face library face_date.pkl
        with open('data/face_date_1.pkl', 'rb') as fr:
            try:
                data = pickle.load(fr)
                self.known_face_encodings = data[0]
                self.known_face_names = data[1]
            except EOFError:
                print("face_date.pkl文件为空")

    def is_success(self, draw):
        """Determine whether the face input is valid"""
        height, width, _ = np.shape(draw)
        rectangles = self.mtcnn_model.detectFace(draw, self.threshold)
        if len(rectangles) == 0:
            return False
        
        # Convert to a square
        rectangles = utils.rect2square(np.array(rectangles, dtype=np.int32))
        rectangles[:, [0, 2]] = np.clip(rectangles[:, [0, 2]], 0, width)
        rectangles[:, [1, 3]] = np.clip(rectangles[:, [1, 3]], 0, height)

        # The detected face can be coded, and multiple faces can be compared
        rectangle = rectangles[0]
        landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
        crop_img = draw[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
        crop_img, _ = utils.Alignment_1(crop_img, landmark)  # Face alignment is carried out using face key points
        crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)
        face_encoding = utils.calc_128_vec(self.facenet_model, crop_img)  # Calculate 128 eigenvalues
        self.known_face_encodings.append(face_encoding)

        return True
            
    def recognize(self, draw):
        """Face recognition  
            Enter: a photo draw  
            In the first step, the MtCNN model is used to locate the face frame  
            The second step, face frame pretreatment (BGR to RGB, resize square, face alignment)  
            The third step is to calculate 128 eigenvalues using the Facenet model  
            The fourth step is to compare the 128 feature values with the database's face data and calculate the score  

        Args:
            draw (<class 'numpy.ndarray'>): Target image to be recognized

        Returns:
            str: Face recognition results
        """

        height, width, _ = np.shape(draw)
        draw_rgb = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
        rectangles = self.mtcnn_model.detectFace(draw_rgb, self.threshold)

        if len(rectangles) == 0:
            return "Unknown"
        
        # Convert to a square
        rectangles = utils.rect2square(np.array(rectangles, dtype=np.int32))
        rectangles[:, [0, 2]] = np.clip(rectangles[:, [0, 2]], 0, width)
        rectangles[:, [1, 3]] = np.clip(rectangles[:, [1, 3]], 0, height)

        # The detected face can be coded, and multiple faces can be compared
        rectangle = rectangles[0]
        landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
        crop_img = draw_rgb[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
        crop_img, _ = utils.Alignment_1(crop_img, landmark)  # Face alignment is carried out using face key points
        crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)
        face_encoding = utils.calc_128_vec(self.facenet_model, crop_img)  # Calculate 128 eigenvalues
            
        # The 128 feature values were compared with the database's face data to calculate the score and select the nearest one  
        face_distances = utils.face_distance(self.known_face_encodings, face_encoding)
        tolerance = 0.6
        name = "Unknown"
        best_match_index = np.argmin(face_distances)
        if face_distances[best_match_index] <= tolerance:
            name = self.known_face_names[best_match_index]

        return name

    def update_face_embeddings(self):
        """Put the newly added face inface_date.pkl"""
        face_name = []
        face_list = os.listdir("data")
        known_face_encodings = []  # known_face_encodings stores the encoded face
        known_face_names = []  # known_face_names stores the names of human
        false_number = 0

        for face in face_list:
            name = face.split(".")[0]
            if name == "face_date" or name == "face_date_1":
                continue
            img = cv2.imread("data/" + face)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            rectangles = self.mtcnn_model.detectFace(img, self.threshold)  # To detect human faces
            rectangles = utils.rect2square(np.array(rectangles))  # Convert to a square
            if len(rectangles):
                rectangle = rectangles[0]
                landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
                crop_img = img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
                try:
                    crop_img, _ = utils.Alignment_1(crop_img, landmark)  # Landmark was used to correct the face
                except cv2.error: 
                    print(face + "更新失败....")
                    continue
                print(face + "...")
                crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)  # Facenet is going to pass in a 160x160 image
                face_encoding = utils.calc_128_vec(self.facenet_model, crop_img)  # The detected face is passed into the Facenet model to realize the extraction of 128-dimensional feature vectors  
                known_face_encodings.append(face_encoding)
                known_face_names.append(name)
                face_name.append(known_face_encodings)
                face_name.append(known_face_names)
                with open("data/face_date.pkl", "wb") as f:
                    pickle.dump(face_name, f)
            else:
                false_number += 1
                print(face + "更新失败....")
                continue
        print("更新失败的个数：", false_number)
