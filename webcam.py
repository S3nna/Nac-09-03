#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv

import cv2
import os,sys, os.path
import numpy as np
import math


def image_da_webcam(img):
    """
    ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems filtrada.
    """
    img = cv2.medianBlur(img,5)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray_rgb = cv2.cvtColor(img_gray,cv2.COLOR_GRAY2BGR)

    # canny = cv2.Canny(img_gray, 60, 100)

    circles =cv2.HoughCircles(img_gray,cv2.HOUGH_GRADIENT, 1.5, 100, param1=100, param2=100, minRadius=50)

    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(img_gray_rgb,(i[0],i[1]),i[2],(0,255,0),2)

    img_hsv = cv2.cvtColor(img_gray_rgb, cv2.COLOR_BGR2HSV)

    image_lower_hsv = np.array([55, 200, 200])  
    image_upper_hsv = np.array([65, 255, 255])

    mask_hsv = cv2.inRange(img_hsv, image_lower_hsv, image_upper_hsv)

    contours, _ = cv2.findContours(mask_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    circulos = img_gray_rgb.copy()

    # coord = np.array([np.int])
    for i in contours:
        
        M = cv2.moments(i)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        
        # coord[i] = cx
        # coord[i + 1] = cy

        size = 20
        color = (128,128,0)
        cv2.line(circulos,(cx - size,cy),(cx + size,cy),color,5)
        cv2.line(circulos,(cx,cy - size),(cx, cy + size),color,5)

        font = cv2.FONT_HERSHEY_SIMPLEX
        text = cy , cx
        if cx <200:
            origem = (cx+100,cy)
        else:
            origem = (cx-400,cy)

        cv2.putText(circulos, str(text), origem, font,1,(200,50,0),2,cv2.LINE_AA)

    # color = (118, 84, 232)
    # cv2.line(circulos, (coord[1] ,coord[2]), (coord[3] ,coord[4]), color, 5)

    # # Calcula angulo
    # circulos_gray = cv2.cvtColor(circulos, cv2.COLOR_BGR2GRAY)
    # edges = cv2.Canny(circulos_gray, 50, 200)

    # lines = cv2.HoughLinesP(edges, 1, math.pi/180.0, 400, np.array([]), 10, 50)

    # hough_img_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

    # for line in lines:
    #     x1, y1, x2, y2 = line[0]
    #     cv2.line(hough_img_rgb, (x1, y1), (x2, y2), (255, 0, 255), 5)

    # angle = math.atan2(y2 - y1, x2 - x1);
    # angle = angle * 180 / np.pi;

    # font = cv2.FONT_HERSHEY_SIMPLEX
    # origem = (40,750)
    # cv2.putText(hough_img_rgb, "Angulo: " + str(180 - angle), origem, font,1,(200,50,0),2,cv2.LINE_AA)

    return circulos

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)


if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    
    img = image_da_webcam(frame)

    cv2.imshow("preview", img)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
