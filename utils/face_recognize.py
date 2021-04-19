import os
import pickle
import cv2
import numpy as np
import utils.utils as utils
from net.inception import InceptionResNetV1
from net.mtcnn import mtcnn


class face_rec():
    def __init__(self):

        self.mtcnn_model = mtcnn()
        self.threshold = [0.5, 0.6, 0.8]
        self.facenet_model = InceptionResNetV1()
        model_path = 'model/facenet_keras.h5'
        self.facenet_model.load_weights(model_path)

        with open('model/face_date.pkl', 'rb') as fr:
            data = pickle.load(fr)
        self.known_face_encodings = data[0]
        # print(type(self.known_face_encodings))
        self.known_face_names = data[1]
        # print(type(self.known_face_names))


    def recognize(self, draw, flag = True):
        # -----------------------------------------------#
        #   人脸识别
        #   先定位，再进行数据库匹配
        # -----------------------------------------------#
        height, width, _ = np.shape(draw)
        draw_rgb = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

        # --------------------------------#
        #   检测人脸
        # --------------------------------#
        rectangles = self.mtcnn_model.detectFace(draw_rgb, self.threshold)

        if len(rectangles) == 0:
            return

        # 转化成正方形
        rectangles = utils.rect2square(np.array(rectangles, dtype=np.int32))
        rectangles[:, [0, 2]] = np.clip(rectangles[:, [0, 2]], 0, width)
        rectangles[:, [1, 3]] = np.clip(rectangles[:, [1, 3]], 0, height)

        # -----------------------------------------------#
        #   对检测到的人脸进行编码
        # -----------------------------------------------#
        face_encodings = []
        for rectangle in rectangles:
            # ---------------#
            #   截取图像
            # ---------------#
            landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
            crop_img = draw_rgb[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            # -----------------------------------------------#
            #   利用人脸关键点进行人脸对齐
            # -----------------------------------------------#
            crop_img, _ = utils.Alignment_1(crop_img, landmark)
            crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)

            face_encoding = utils.calc_128_vec(self.facenet_model, crop_img)
            face_encodings.append(face_encoding)

        face_names = []
        for face_encoding in face_encodings:
            # -------------------------------------------------------#
            #   取出一张脸并与数据库中所有的人脸进行对比，计算得分
            # -------------------------------------------------------#
            # matches = utils.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.7)
            name = "Unknown"
            # -------------------------------------------------------#
            #   找出距离最近的人脸
            # -------------------------------------------------------#
            face_distances = utils.face_distance(self.known_face_encodings, face_encoding)
            # -------------------------------------------------------#
            #   取出这个最近人脸的评分
            # -------------------------------------------------------#
            tolerance = 0.6
            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] <= tolerance:
                name = self.known_face_names[best_match_index]
                global ultimate_name
                ultimate_name = name
            face_names.append(name)

        rectangles = rectangles[:, 0:4]
        # -----------------------------------------------#
        #   画框~!~
        # -----------------------------------------------#
        if flag:
            for (left, top, right, bottom), name in zip(rectangles, face_names):
                cv2.rectangle(draw, (left, top), (right, bottom), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(draw, name, (left, bottom - 15), font, 0.75, (255, 255, 255), 2)
        return draw


ddd = face_rec()

mtcnn_model = mtcnn()
threshold = [0.5, 0.6, 0.8]
facenet_model = InceptionResNetV1()
model_path = 'model/facenet_keras.h5'
facenet_model.load_weights(model_path)


def return_name(img):
    height, width, _ = np.shape(img)
    # draw_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    draw_rgb = img
    rectangles = mtcnn_model.detectFace(draw_rgb, threshold)

    if len(rectangles) == 0:
        return

    # 转化成正方形
    rectangles = utils.rect2square(np.array(rectangles, dtype=np.int32))
    rectangles[:, [0, 2]] = np.clip(rectangles[:, [0, 2]], 0, width)
    rectangles[:, [1, 3]] = np.clip(rectangles[:, [1, 3]], 0, height)

    rectangle = rectangles[0]
    landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
    crop_img = draw_rgb[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
    crop_img, _ = utils.Alignment_1(crop_img, landmark)
    crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)
    face_encoding = utils.calc_128_vec(facenet_model, crop_img)
    name = "Unknown"
    face_distances = utils.face_distance(ddd.known_face_encodings, face_encoding)

    tolerance = 0.6
    best_match_index = np.argmin(face_distances)
    if face_distances[best_match_index] <= tolerance:
        name = ddd.known_face_names[best_match_index]
    face_name = name
    return face_name


if __name__ == "__main__":
    # dududu = face_rec()
    # video_capture = cv2.VideoCapture(r"E:\Pycharm Projects\DeepLearning\tttt\output1.avi")
    # ret, draw = video_capture.read()
    # writer = cv2.VideoWriter('output__1.avi', cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 30, (640, 480))
    # while ret:
    #
    #     # draw = cv2.flip(draw, 1)
    #     dududu.recognize(draw)
    #
    #     # cv2.imshow('Video', draw)
    #     writer.write(draw)
    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #         break
    #     ret, draw = video_capture.read()
    #
    # video_capture.release()
    # cv2.destroyAllWindows()
    dududu = face_rec()
    video_capture = cv2.VideoCapture(0)
    dududu = face_rec()
    while True:
        ret, draw = video_capture.read()
        draw = cv2.flip(draw, 1)
        dududu.recognize(draw)

        cv2.imshow('Video', draw)
        if cv2.waitKey(60) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
