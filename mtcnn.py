import cv2
import numpy as np
from keras.layers import Activation, Conv2D, Dense, Flatten, Input, MaxPool2D, Permute, Reshape
from keras.layers.advanced_activations import PReLU
from keras.models import Model, Sequential
import utils


def create_Pnet(weight_path):
    """
    搭建Pnet网络，粗略获取人脸框, 输出bbox位置和是否有人脸
    """
    inputs = Input(shape=[None, None, 3])

    x = Conv2D(10, (3, 3), strides=1, padding='valid', name='conv1')(inputs)
    x = PReLU(shared_axes=[1, 2], name='PReLU1')(x)
    x = MaxPool2D(pool_size=2)(x)

    x = Conv2D(16, (3, 3), strides=1, padding='valid', name='conv2')(x)
    x = PReLU(shared_axes=[1, 2], name='PReLU2')(x)

    x = Conv2D(32, (3, 3), strides=1, padding='valid', name='conv3')(x)
    x = PReLU(shared_axes=[1, 2], name='PReLU3')(x)

    classifier = Conv2D(2, (1, 1), activation='softmax', name='conv4-1')(x)
    bbox_regress = Conv2D(4, (1, 1), name='conv4-2')(x)

    model = Model([inputs], [classifier, bbox_regress])
    model.load_weights(weight_path, by_name=True)
    return model


def create_Rnet(weight_path):
    """
    搭建Rnet网络，同时精修框
    """
    inputs = Input(shape=[24, 24, 3])

    x = Conv2D(28, (3, 3), strides=1, padding='valid', name='conv1')(inputs)
    x = PReLU(shared_axes=[1, 2], name='prelu1')(x)
    x = MaxPool2D(pool_size=3, strides=2, padding='same')(x)

    x = Conv2D(48, (3, 3), strides=1, padding='valid', name='conv2')(x)
    x = PReLU(shared_axes=[1, 2], name='prelu2')(x)
    x = MaxPool2D(pool_size=3, strides=2)(x)

    x = Conv2D(64, (2, 2), strides=1, padding='valid', name='conv3')(x)
    x = PReLU(shared_axes=[1, 2], name='prelu3')(x)

    x = Permute((3, 2, 1))(x)
    x = Flatten()(x)

    x = Dense(128, name='conv4')(x)
    x = PReLU(name='prelu4')(x)

    classifier = Dense(2, activation='softmax', name='conv5-1')(x)
    bbox_regress = Dense(4, name='conv5-2')(x)
    model = Model([inputs], [classifier, bbox_regress])
    model.load_weights(weight_path, by_name=True)
    return model


def create_Onet(weight_path):
    """
    搭建Onet网络，再次精修框并获得五个点
    """
    inputs = Input(shape=[48, 48, 3])

    x = Conv2D(32, (3, 3), strides=1, padding='valid', name='conv1')(inputs)
    x = PReLU(shared_axes=[1, 2], name='prelu1')(x)
    x = MaxPool2D(pool_size=3, strides=2, padding='same')(x)

    x = Conv2D(64, (3, 3), strides=1, padding='valid', name='conv2')(x)
    x = PReLU(shared_axes=[1, 2], name='prelu2')(x)
    x = MaxPool2D(pool_size=3, strides=2)(x)

    x = Conv2D(64, (3, 3), strides=1, padding='valid', name='conv3')(x)
    x = PReLU(shared_axes=[1, 2], name='prelu3')(x)
    x = MaxPool2D(pool_size=2)(x)

    x = Conv2D(128, (2, 2), strides=1, padding='valid', name='conv4')(x)
    x = PReLU(shared_axes=[1, 2], name='prelu4')(x)

    x = Permute((3, 2, 1))(x)
    x = Flatten()(x)

    x = Dense(256, name='conv5')(x)
    x = PReLU(name='prelu5')(x)

    classifier = Dense(2, activation='softmax', name='conv6-1')(x)
    bbox_regress = Dense(4, name='conv6-2')(x)
    landmark_regress = Dense(10, name='conv6-3')(x)

    model = Model([inputs], [classifier, bbox_regress, landmark_regress])
    model.load_weights(weight_path, by_name=True)
    return model


class MTCNN():
    """
    MTCNN 的作用是获取人脸图像框。
    首先照片会按照不同的缩放比例，缩放成不同大小的图片，形成图片的特征金字塔。
    PNet 主要获得了人脸区域的候选窗口和边界框的回归向量。并用该边界框做回归，对候选窗口进行校准，然后通过非极大值抑制（NMS）来合并高度重叠的候选框。
    RNet 将经过 PNet 的候选框在 RNet 网络中训练，然后利用边界框的回归值微调候选窗体，再利用 NMS 去除重叠窗体。
    ONet 功能与 RNet 作用类似，只是在去除重叠候选窗口的同时，同时显示五个人脸关键点定位（眼睛、嘴角、鼻尖）。
    """
    def __init__(self):
        """
        初始化 MTCNN 网络，搭建 P-Net、R-Net、O-Net
        """
        self.Pnet = create_Pnet('model/pnet.h5')
        self.Rnet = create_Rnet('model/rnet.h5')
        self.Onet = create_Onet('model/onet.h5')

    def detectFace(self, img, threshold):
        """
        检测脸部，获取人脸检测框
        """
        copy_img = (img.copy() - 127.5) / 127.5  # 归一化
        origin_h, origin_w, _ = copy_img.shape  # 原始图像大小
        scales = utils.calculateScales(img)  # 计算原始输入图像缩放的比例

        #-------------------------------------------------#
        # pnet部分：粗略计算人脸框
        # 先粗略预测，存放到 out 
        # 然后进行解码预测，生成人脸框（粗略坐标），存放到 rectangles
        #-------------------------------------------------#
        out = []
        rectangles = []
        for scale in scales:
            hs = int(origin_h * scale)  # 缩放
            ws = int(origin_w * scale)  # 缩放
            scale_img = cv2.resize(copy_img, (ws, hs))
            inputs = np.expand_dims(scale_img, 0)
            ouput = self.Pnet.predict(inputs)
            ouput = [ouput[0][0], ouput[1][0]]  # 一张图片二维图，消除第三维数据
            out.append(ouput)
        for i in range(len(scales)):
            cls_prob = out[i][0][:, :, 1]
            out_h, out_w = cls_prob.shape
            out_side = max(out_h, out_w)
            roi = out[i][1]
            rectangle = utils.detect_face_12net(cls_prob, roi, out_side, 1 / scales[i], origin_w, origin_h, threshold[0])  # 解码
            rectangles.extend(rectangle)

        rectangles = np.array(utils.NMS(rectangles, 0.7))  # 非极大抑制

        if len(rectangles) == 0:
            print("没有检测到人脸")
            return

        #--------------------------------------#
        # Rnet部分：稍微精确计算人脸框
        # 最后将人脸框转化为正方形
        #--------------------------------------#
        predict_24_batch = []
        for rectangle in rectangles:
            crop_img = copy_img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]  # 利用获取到的粗略坐标，在原图上进行截取
            scale_img = cv2.resize(crop_img, (24, 24))
            predict_24_batch.append(scale_img)
        
        cls_prob, roi_prob = self.Rnet.predict(np.array(predict_24_batch))

        rectangles = utils.filter_face_24net(cls_prob, roi_prob, rectangles, origin_w, origin_h, threshold[1])  # 解码

        if len(rectangles) == 0:
            return rectangles

        #-----------------------------#
        # Onet部分：计算人脸框
        # 输出五个人脸关键点定位（眼睛、嘴角、鼻尖）
        #-----------------------------#
        predict_batch = []
        for rectangle in rectangles:
            crop_img = copy_img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]  # 利用获取到的粗略坐标，在原图上进行截取
            scale_img = cv2.resize(crop_img, (48, 48))
            predict_batch.append(scale_img)
        
        cls_prob, roi_prob, pts_prob = self.Onet.predict(np.array(predict_batch))

        rectangles = utils.filter_face_48net(cls_prob, roi_prob, pts_prob, rectangles, origin_w, origin_h, threshold[2])  # 解码

        return rectangles
