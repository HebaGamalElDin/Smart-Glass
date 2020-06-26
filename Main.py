# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 06:55:29 2020

@author: Heba Gamal El-Din
"""

from Detiction import ObjectRecognition
from TextToSpeach import TextToSpeach
import time
import cv2
from OCRModels import OCR


if __name__ == '__main__':
    """ Opening Web Camera """
    Cap = cv2.VideoCapture(0)
    FPS = Cap.get(cv2.CAP_PROP_FPS)
    KPS = 5
    hop = round(FPS / KPS)
    curr_frame = 0
    print(FPS)
    time.sleep(1)
    Writer = None
    Speaker = TextToSpeach()
    Recognizer = ObjectRecognition()
    if input("Type Start To Start ::: ") == "Start":
        (Bool, Frame) = Cap.read()
        if not Bool:
            print("Camera Resouce Not Found")
        else:
            if curr_frame % hop == 0:
                Texts, Objects_ = Recognizer.Recognizer_(Frame)
                cv2.imshow("Live Video", Frame)
                Speaker.Speaker_(Texts)
                cv2.imwrite('Scene.png', Frame)
                curr_frame+=1
            CV = cv2.waitKey(3)
            if CV & 0xFF == ord('q'):
                Speaker.engine.stop()
    elif input("Read Mode ::: ") == "Read":
        while Cap.isOpened():
            (Bool, Frame) = Cap.read()
            if not Bool:
                print("Camera Resouce Not Found")
                break
            else:
                OCR(Frame)
        print("[INFO] Ending with cleaning up...")  
        Cap.release()
        cv2.destroyAllWindows()
