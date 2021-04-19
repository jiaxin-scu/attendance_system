import os
import pickle
import cv2
import numpy as np
import utils.utils as utils
from net.inception import InceptionResNetV1
from net.mtcnn import mtcnn


def update_face_embeddings():
    face_name = []
    mtcnn_model = mtcnn()
    threshold = [0.5, 0.6, 0.8]

    facenet_model = InceptionResNetV1()
    model_path = 'model/facenet_keras.h5'
    facenet_model.load_weights(model_path)

    # -----------------------------------------------#
    #   对数据库中的人脸进行编码
    #   known_face_encodings中存储的是编码后的人脸
    #   known_face_names为人脸的名字
    # -----------------------------------------------#
    face_list = os.listdir("dataset")
    known_face_encodings = []
    known_face_names = []
    for face in face_list:
        name = face.split(".")[0]
        img = cv2.imread("dataset/" + face)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # ---------------------#
        #   检测人脸
        # ---------------------#
        rectangles = mtcnn_model.detectFace(img, threshold)
        # ---------------------#
        #   转化成正方形
        # ---------------------#
        rectangles = utils.rect2square(np.array(rectangles))
        # -----------------------------------------------#
        #   facenet要传入一个160x160的图片
        #   利用landmark对人脸进行矫正
        # -----------------------------------------------#
        rectangle = rectangles[0]
        landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
        crop_img = img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
        crop_img, _ = utils.Alignment_1(crop_img, landmark)
        crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)
        # --------------------------------------------------------------------#
        #   将检测到的人脸传入到facenet的模型中，实现128维特征向量的提取
        # --------------------------------------------------------------------#
        face_encoding = utils.calc_128_vec(facenet_model, crop_img)

        known_face_encodings.append(face_encoding)
        known_face_names.append(name)
        face_name.append(known_face_encodings)
        face_name.append(known_face_names)
        with open("model/face_date.pkl", "wb") as f:
            pickle.dump(face_name, f)


if __name__ == '__main__':
    update_face_embeddings()
