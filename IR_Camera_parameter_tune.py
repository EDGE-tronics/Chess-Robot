import VisionModule as vm
import stream_tinker as depthCam
#import requests
import time
import winsound
import cv2
import os
import socket, keepalive
import numpy as np
route = os.getcwd() + '/'

homography = []
curIMG = []
RGBIMG = []
rotMat = vm.np.zeros((2,2))
count_captures = 0

def takePIC_RGB():  
    global selectedCam
    global cap
    
    #requests.delete("http://192.168.233.1")
    #time.sleep(2)
    depthCam.post_encode_config(depthCam.frame_config_encode(1, 1, 255, 1, 2, 7, 1, 0, 0))

    for i in range(2):                    # Clear images stored in buffer
        time.sleep(.02) 
        p = depthCam.get_frame_from_http()
        frame = depthCam.load_frame_RGB(p)
    
#     freq = 500
#     dur = 100
#     winsound.Beep(freq,dur)
    
    return frame

def takePIC_IR():  
    global selectedCam
    global cap
    

    #depthCam.post_encode_config(depthCam.frame_config_encode(1, 1, 255, 1, 2, 7, 1, 0, 0))

    for i in range(2):                    # Clear images stored in buffer      
        time.sleep(.02)
        p = depthCam.get_frame_from_http()
        frame = depthCam.load_frame_IR(p)
    
    return frame

#keepalive.set(socket, after_idle_sec=60, interval_sec=60, max_fails=5)
#socket.SIO_KEEPALIVE_VALS, (1,  20000, 1000)


# Homography calcs with RGB image - NEEDS BLANK BOARD!
cbPattern = cv2.imread(route+'interface_images/cb_pattern.jpg', cv2.IMREAD_GRAYSCALE)
frame = takePIC_RGB()
retIMG, homography = vm.findTransformation(frame,cbPattern)
depthCam.post_encode_config(depthCam.frame_config_encode(1, 1, 255, 1, 2, 7, 1, 0, 0))
            
while True:
    # Capture IR image, apply homography and contrast 
    #time.sleep(3)
    curIMG = takePIC_IR()
    curIMG = vm.applyHomography(curIMG,homography)
    curIMG = vm.applyRotation(curIMG,rotMat)
    normalized_mask = np.zeros((800, 800))
    normalizedIR = cv2.normalize(curIMG,  normalized_mask, 100,400 , cv2.NORM_MINMAX)
    histIR = cv2.equalizeHist(normalizedIR)

    RGBIMG = takePIC_RGB()
    RGBIMG = vm.applyHomography(RGBIMG,homography)
    RGBIMG = vm.applyRotation(RGBIMG,rotMat)
    normalizedRGB = cv2.normalize(RGBIMG,  normalized_mask, 100,300 , cv2.NORM_MINMAX)
    histRGB = cv2.cvtColor(RGBIMG, cv2.COLOR_BGR2GRAY)
    histRGB = cv2.equalizeHist(histRGB)
    
    alpha = 0.5
    beta = (1.0 - alpha)
    combinned = cv2.addWeighted(histIR, alpha, histRGB, beta, 0.0)
    combinned_norm = cv2.norm(histIR,histRGB)
    
    count_captures += 1
    print(count_captures)

#    cv2.imshow('curIMG', curIMG)                
#    cv2.imshow('RGBIMG', RGBIMG)
    cv2.imshow('normalizedIR', normalizedIR)
    cv2.imshow('normalizedRGB', normalizedRGB)
    cv2.imshow('HistIR', histIR)
    cv2.imshow('HistRGB', histRGB)
    cv2.imshow('Combinned_add', combinned)
    cv2.imshow('Combinned_norm', combinned_norm)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
