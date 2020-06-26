# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 05:27:01 2020

@author: Heba Gamal EL-Din
"""

from PIL import Image
import pytesseract
import cv2
import time 

class OCR:
    def __init__(self, Frame):
        self.Frame = Frame
        self.Height = Frame.shape[0]
        self.Width = Frame.shape[1]
        self.OCR_()
        
    def OCR_(self):
        img = cv2.resize(self.Frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                                                               
        gray = cv2.medianBlur(gray, 3)
        gray = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        text = ''
        Flag = None
        if Flag is None:
            Text = pytesseract.image_to_string(Image.fromarray(gray), lang="eng+ara", config='--oem 1 --psm 3')
            if len(Text) > 0:  
                Flag = "Eng"
                print(str(len(Text)) + " Eng")
                print (Text)
                text = Text
                return text
        elif len(text) == 0:
            return "No Text Recognized! "

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    FPS = cap.get(cv2.CAP_PROP_FPS)
    KPS = 5
    hop = round(FPS / KPS)
    curr_frame = 0
    print(FPS)
    while True: 
        ret, Frame = cap.read()
        if curr_frame % hop == 0:
            OCR(Frame)
            cv2.imshow('Frame', Frame)   
        curr_frame+=1
        CV = cv2.waitKey(1)
        if CV == 27:
            break
    print("[INFO] cleaning up...")  
    cap.release()           ## After Ending, Release The Camera Resourse Usage
    cv2.destroyAllWindows() ## And Destroy All Opened Windows    
        