import os
import pickle
import cv2
import numpy as np
import utils
from inception import InceptionResNetV1
import mtcnn


class face_rec():
    """
    人脸识别的主要类
    """

    def __init__(self):
        """
        初始化
        mtcnn_model：mtcnn 模型，用于提取人脸框，输出 5 个关键点（双眼、嘴角、鼻尖）
        facenet_model：人脸识别模型，输出 128 个人脸特征点
        """
        self.mtcnn_model = mtcnn.MTCNN()
        self.threshold = [0.5, 0.6, 0.8]
        self.facenet_model = InceptionResNetV1()
        model_path = 'model/facenet_keras.h5'
        self.facenet_model.load_weights(model_path)
        self.known_face_encodings = []
        self.known_face_names = []

        # 导入人脸库 face_date.pkl
        with open('data/face_date.pkl', 'rb') as fr:
            try:
                data = pickle.load(fr)
                self.known_face_encodings = data[0]
                self.known_face_names = data[1]
            except EOFError:
                print("face_date.pkl文件为空")

    def is_success(self, draw):
        """
        判断录入的人脸是否有效
        """
        height, width, _ = np.shape(draw)
        rectangles = self.mtcnn_model.detectFace(draw, self.threshold)
        if len(rectangles) == 0:
            return False
        
        # 转化成正方形
        rectangles = utils.rect2square(np.array(rectangles, dtype=np.int32))
        rectangles[:, [0, 2]] = np.clip(rectangles[:, [0, 2]], 0, width)
        rectangles[:, [1, 3]] = np.clip(rectangles[:, [1, 3]], 0, height)

        # 对检测到的人脸进行编码，可以进行多张人脸比对
        rectangle = rectangles[0]
        landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
        crop_img = draw[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
        crop_img, _ = utils.Alignment_1(crop_img, landmark)  # 利用人脸关键点进行人脸对齐
        crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)
        face_encoding = utils.calc_128_vec(self.facenet_model, crop_img)  # 计算 128 特征值
        self.known_face_encodings.append(face_encoding)

        return True
            
    def recognize(self, draw, flag=True):
        """
        人脸识别
        输入：一张照片 draw
        第一步，使用 mtcnn 模型定位人脸框
        第二步，人脸框预处理（BGR转RGB、resize正方形、人脸对齐）
        第三步，使用 facenet 模型计算 128 特征值
        第四步，将这 128 个特征值和数据库的人脸数据进行比对，计算得分
        """
        height, width, _ = np.shape(draw)
        draw_rgb = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
        rectangles = self.mtcnn_model.detectFace(draw_rgb, self.threshold)

        if len(rectangles) == 0:
            return "Unknown"
        
        # 转化成正方形
        rectangles = utils.rect2square(np.array(rectangles, dtype=np.int32))
        rectangles[:, [0, 2]] = np.clip(rectangles[:, [0, 2]], 0, width)
        rectangles[:, [1, 3]] = np.clip(rectangles[:, [1, 3]], 0, height)

        # 对检测到的人脸进行编码，可以进行多张人脸比对
        rectangle = rectangles[0]
        landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
        crop_img = draw_rgb[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
        crop_img, _ = utils.Alignment_1(crop_img, landmark)  # 利用人脸关键点进行人脸对齐
        crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)
        face_encoding = utils.calc_128_vec(self.facenet_model, crop_img)  # 计算 128 特征值
            
        # 将这 128 个特征值和数据库的人脸数据进行比对，计算得分，选择距离最近的
        face_distances = utils.face_distance(self.known_face_encodings, face_encoding)
        tolerance = 0.6
        name = "Unknown"
        best_match_index = np.argmin(face_distances)
        if face_distances[best_match_index] <= tolerance:
            name = self.known_face_names[best_match_index]

        return name

    def update_face_embeddings(self):
        """
        将新添加的人脸放入 face_date.pkl
        """
        face_name = []
        face_list = os.listdir("data")
        known_face_encodings = []  # known_face_encodings中存储的是编码后的人脸
        known_face_names = []  # known_face_names为人脸的名字

        for face in face_list:
            name = face.split(".")[0]
            if name == "face_date":
                continue
            img = cv2.imread("data/" + face)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            rectangles = self.mtcnn_model.detectFace(img, self.threshold)  # 检测人脸
            rectangles = utils.rect2square(np.array(rectangles))  # 转化成正方形
            rectangle = rectangles[0]
            landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
            crop_img = img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            crop_img, _ = utils.Alignment_1(crop_img, landmark)  # 利用 landmark 对人脸进行矫正
            crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)  # facenet要传入一个 160x160 的图片
            face_encoding = utils.calc_128_vec(self.facenet_model, crop_img)  # 将检测到的人脸传入到 facenet 的模型中，实现 128 维特征向量的提取
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)
            face_name.append(known_face_encodings)
            face_name.append(known_face_names)
            with open("data/face_date.pkl", "wb") as f:
                pickle.dump(face_name, f)
