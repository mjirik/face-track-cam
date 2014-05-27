# -*- coding: utf-8 -*-
"""
Created on Tue May 06 21:11:51 2014

@author: Martin
"""
import serial
import time
import math
import matplotlib.pyplot as plt
import numpy as np
import cv2
from numpy import arange
import scipy.misc
from scipy.misc import imrotate

arduino = serial.Serial('COM4', 57600)
time.sleep(2) # waiting the initialization...
startH = 70
startV = 70
cesta = str(startH)+'h'+str(startV)+'v'
arduino.write(cesta)
ociX = []
ociY = []
uhelOci = 0
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
scale = arange(1.0, 2.1, 0.1) 
while(True):
    ret, frame = cap.read()
    img = frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    Y,X = gray.shape
    StredX = X/2
    StredY = Y/2
    cv2.rectangle(img,(StredX-2,StredY-2),(StredX+2,StredY+2),(0,0,255),2)
    #cv2.rectangle(img,(StredX-40,StredY-40),(StredX+40,StredY+40),(150,150,0),2)
    obsah = []
    faces = face_cascade.detectMultiScale(gray,1.2,5)
    if not(len(faces)==0):
        for (x,y,w,h) in faces:
            obsah.append(w*h)
        maximum = max(obsah) 
        pozice = argmax(obsah)
        (x,y,w,h) = faces[pozice]
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        StredRecX = x+(h/2)
        StredRecY = y+(h/2)
        cv2.rectangle(img,(StredRecX-2,StredRecY-2),(StredRecX+2,StredRecY+2),(0,0,255),2) 
        posunX = (StredX-StredRecX)
        posunY = (StredY-StredRecY)
        if(abs(posunX)>40)|(abs(posunY)>40):
            if(posunX>5):
                startV = startV+1
            elif(posunX<5):
                startV = startV-1  
            if(posunY>5):
                startH = startH-1
            elif(posunY<5):
                startH = startH+1
            cesta = (str(startH)+'h'+str(startV)+'v')
            arduino.write(cesta)
            while(True):
                if(arduino.read()=='1'):
                    break
        scale = arange(1.3, 2.1, 0.1) 
        for index in scale:
            eyes = eye_cascade.detectMultiScale(roi_gray,index,5)
            if (len(eyes) == 2):
                ociX = []
                ociY = []
                for (ex,ey,ew,eh) in eyes:
                    ociX.append(ex+(eh/2))
                    ociY.append(ey+(ew/2))
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                cv2.line(roi_color,(ociX[0],ociY[0]),(ociX[1],ociY[1]),(0,0,255),2)
                if(ociX[0]>ociX[1]):   
                    uhelOci = math.atan2(ociY[0]-ociY[1],ociX[0]-ociX[1])   
                else:
                    uhelOci = math.atan2(ociY[1]-ociY[0],ociX[1]-ociX[0])
                #stupneN = math.degrees(cislo)
                #rozdil = stupneN-stupne
                break        
    cv2.imshow('img',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
arduino.close() #say goodbye to Arduino