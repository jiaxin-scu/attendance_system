import face_recognize
import os
import cv2
import requests


def update():
    face_check = face_recognize.face_rec()
    face_check.update_face_embeddings()


def test_acc():
    recognized_num = 0
    not_recognized_num = 0
    face_check = face_recognize.face_rec()
    face_list = os.listdir("test")
    for i in face_list:
        img = cv2.imread("test/" + i)
        img = cv2.flip(img, 1)
        name = face_check.recognize(img)
        if name + ".jpg" == i:
            recognized_num += 1
            print(i + " successfully resognized.")
        else:
            not_recognized_num += 1
            print(i + " can not resognized.")
    acc = recognized_num / (recognized_num + not_recognized_num)
    print("recognized_num: " + str(recognized_num))
    print("not_recognized_num: " + str(not_recognized_num))
    print("acc: " + str(acc))


def test_api_post():
    response = requests.post("https://vignetting.work/record" + "?studentId=1&classRoomId=1")
    result = response.json()
    print(result)

def test_api_get():
    response = requests.get("https://vignetting.work/student/" + "1")
    result = response.json()
    print(result)

update()
