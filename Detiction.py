# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 05:59:34 2020

@author: Heba Gamal El-Din
"""
import numpy as np
import imutils
import time
import cv2

class ObjectRecognition:
    def __init__(self):
        self.Net = self.Get_OutLayer()[0]
        self.OutLayers = self.Get_OutLayer()[1]
        """ Important Variables """
        self.Writer = None
        (self.W, self.H) = (None, None)
        self.Scale = 1 / 255.0
        self.Confidence_Threshold = 0.5
        self.NMS_Threshold = 0.4     
        self.Camera_Focal_Length = 522.85 ## Inches
        self.KNOWN_WIDTH = {'person' : 16.5354, 'bed' : 106.299, 'cup' : 3.93701, 'cell phone' : 4.72441, 'chair' : 18.8976}        ## Inches

    
    """                           Backend Methods                              """
    #####################################
    """ Objects.txt Is A File 
    Contains All Objects Can be Detected 
        by YOLO Pre-Trained Model """
    #####################################
    np.random.seed(42)
    Objects = None
    with open('Objects.txt', 'r') as f:  ## Reading Objects' Names File
        Objects = [line.strip() for line in f.readlines()]
    COLORS = np.random.randint(0, 255, size=(len(Objects), 3),dtype="uint8") ## Random Rectangle COLOR For Each Object From The 80's
        
    """ Starter Voice """
    """def beep() :
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))"""
    
    ###########################################
    """ Establishment OF YOLO Pre-Trained Model 
        BY Its Configuration File """
    ##########################################
    def Network_Establish(self):
        Net = cv2.dnn.readNet("yolov3.cfg", "yolov3.weights")
        return Net
    
    ####################################
    """ Getting The Output Layer Of
            The Network """
    ####################################
    def Get_OutLayer(self):   
        net = self.Network_Establish()
        outlayer = net.getLayerNames()
        outlayer = [outlayer[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return net,outlayer
    
    #Net, OutLayers = Get_OutLayer() ## Out Of The Class
    #######################################
    """ Feeding The Frame to The Network &
             Get Its Output """
    #######################################
    def Frame_Processing(self, Frame):    
        Blob = cv2.dnn.blobFromImage(Frame, self.Scale, (416,416), swapRB=True, crop=False)
        self.Net.setInput(Blob)
        self.Output_Layers = self.Net.forward(self.OutLayers) 
        return self.Output_Layers
    
    ########################################
    """ Specify Attributes For The Final 
    Detected Objects to be Displayed """
    #######################################
    def Detections_Attributes(self,layerOutputs):
        Objescts_IDs = []
        Confidences = []
        boxes = []
        Centers = []
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                Obj_ID = np.argmax(scores)
                confidence = scores[Obj_ID]
                if confidence > self.Confidence_Threshold:
                    """Boxes' Points"""
                    box = detection[0:4] * np.array([self.W, self.H, self.W, self.H])
                    (centerX, centerY, width, height) = box.astype("int")
                    X = int(centerX - (width / 2))
                    Y = int(centerY - (height / 2))
                    Objescts_IDs.append(Obj_ID)
                    Confidences.append(confidence.astype("float"))
                    boxes.append([X, Y, int(width), int(height)])
                    Centers.append((centerX,centerY))
        return boxes, Confidences, Objescts_IDs, Centers
    
    #############################
    """ Distance Calculating """
    ############################
    def distance_to_camera(self, knownWidth, focalLength, Pixels_width):
        return (knownWidth * focalLength) / Pixels_width
    
    #######################################
    """" Non-Maximum Suppression Function 
    Avoids The Problem Of Overlapped Box 
    Around The Same Detected Object"""
    #######################################
    def Non_Max_Suppresion(self,Frame, Boxes, Confidences, Objescts_IDs, Centers):
        Detected_objects = []
        texts = []
        Indecies = cv2.dnn.NMSBoxes(Boxes, Confidences, self.Confidence_Threshold, self.NMS_Threshold)
        if len(Indecies) > 0:
            for i in Indecies.flatten():
                (x,y) = (Boxes[i][0], Boxes[i][1])
                (w,h) = (Boxes[i][2], Boxes[i][3])
                print(w)
                Colors = [int(c) for c in self.COLORS[Objescts_IDs[i]]]
                Obj = self.Objects[Objescts_IDs[i]]
                
                if Obj in list(self.KNOWN_WIDTH.keys()):
                    Orig_Width = self.KNOWN_WIDTH[Obj]
                    DIS = (float(self.distance_to_camera(Orig_Width, self.Camera_Focal_Length, w)) * 2.54) / 100 #* 0.0328084
                else:
                    DIS = (((2 * 3.14 * 180) / (w + h * 360) * 1000 + 3) * 2.54) / 100
                cv2.rectangle(Frame, (x,y), (x+w,y+h), Colors, 2)
                cv2.putText(Frame, Obj + ' Confidence:: %.2f' % Confidences[i], (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, Colors, 2)
                if Obj not in Detected_objects:
                    centerX, centerY = Centers[i][0], Centers[i][1]
                    if centerX <= self.W/3:
                        W_pos = "left"
                    elif centerX <= (self.W/3 *2):
                        W_pos = "Forward"
                    else:
                        W_pos = "right"
                    if centerY <= self.W/3:
                        H_pos = "top"
                    elif centerY <= (self.W/3 *2):
                        H_pos = "Direct"
                    else:
                        H_pos = "bottom"                
                    Detected_objects.append(self.Objects[Objescts_IDs[i]])    
                    texts.append("A " + Obj + " Found Away From You Approximatilly {:.1f}".format(DIS) + " Meters" + " In The " + H_pos + " " + W_pos)
        return texts, Detected_objects

    ############################
    """ Recognition PipeLine """
    ############################
    def Recognizer_(self,Frame):
        if self.W is None or self.H is None:
            (self.H,self.W) = Frame.shape[:2]
        Output_Layers = self.Frame_Processing(Frame)
        (Boxes, Confidences, Objescts_IDs, Centers) = self.Detections_Attributes(Output_Layers)
        Texts, Objs = self.Non_Max_Suppresion(Frame, Boxes, Confidences,Objescts_IDs, Centers)
        return Texts, Objs