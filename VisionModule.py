import cv2
import numpy as np
import string
import time
import os

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    pass

def findTransformation(img,cbPattern):

    patternSize = (7,7)
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    retCB, cornersCB = cv2.findChessboardCorners(cbPattern, patternSize, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    retIMG, cornersIMG = cv2.findChessboardCorners(imgGray, patternSize, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    
    if retIMG == 0:
        H = 0
    else:
        H, _ = cv2.findHomography(cornersIMG, cornersCB)     # Find the transformation matrix
    
    return(retIMG, H)

def applyRotation(img,R):
    if R.any() != 0:
        img = cv2.warpAffine(img, R, img.shape[1::-1], flags=cv2.INTER_LINEAR)
        
    return(img)

def applyHomography(img,H):

    imgNEW = cv2.warpPerspective(img, H, (400, 400))
    
    return(imgNEW)

def drawQuadrants(img):

    # Draw quadrants and numbers on image
    imgquad = img.copy()
    cv2.line(imgquad, (200, 0), (200, 400), (0,255,0), 3)
    cv2.line(imgquad, (0, 200), (400, 200), (0,255,0), 3)
    imgquad = cv2.putText(imgquad, '1', (80, 120) , cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3, cv2.LINE_AA)
    imgquad = cv2.putText(imgquad, '2', (280, 120) , cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3, cv2.LINE_AA) 
    imgquad = cv2.putText(imgquad, '3', (280, 320) , cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3, cv2.LINE_AA) 
    imgquad = cv2.putText(imgquad, '4', (80, 320) , cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3, cv2.LINE_AA) 

    return(imgquad)

def findRotation(theta):

    if theta != 0:
        rotMAT = cv2.getRotationMatrix2D(tuple(np.array((400,400)[1::-1])/2), theta, 1.0)
    else:
        rotMAT = np.zeros((2,2))

    return(rotMAT)

def findMoves(img1, img2):

    size = 50
    img1SQ = img2SQ = []
    largest = [0, 0, 0, 0]
    coordinates = [0, 0, 0, 0]
    for y in range(0,8*size,size):
        for x in range(0,8*size,size):
            img1SQ = img1[x:x+size, y:y+size]
            img2SQ = img2[x:x+size, y:y+size]
            dist = cv2.norm(img2SQ, img1SQ)
            for z in range(0,4):
                if dist >= largest[z]:
                    largest.insert(z,dist)
                    # Save in algebraic chess notation
                    coordinates.insert(z,(string.ascii_lowercase[int(x/size)]+str(int(y/size+1))))
                    largest.pop()
                    coordinates.pop()
                    break

    # Make threshold with a percentage of the change in color of the biggest two
    thresh = (largest[0]+largest[1])/2*(0.5)
    for t in range(3,1,-1):
        if largest[t] < thresh:
            coordinates.pop()
    
    return(coordinates)

def safetoMove(H, cap, selectedCam):

    cbPattern = cv2.imread(os.getcwd() + '/' +'interface_images/cb_pattern.jpg', cv2.IMREAD_GRAYSCALE)

    if selectedCam:
        for i in range(5):                    # Clear images stored in buffer
            cap.grab()
        _ , img = cap.read()                  # USB Cam
    else:
        rawCapture = PiRGBArray(cap, size=(640, 480))
        cap.capture(rawCapture, format="bgr") # RPi Cam
        img = rawCapture.array
        rawCapture.truncate(0)                # Clear the stream in preparation for the next image

    img = cv2.warpPerspective(img, H, (cbPattern.shape[1], cbPattern.shape[0]))

    # Kmeans algorithm (Map the image to only two colors)
    K = 2
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    Z = np.float32(img.reshape((-1,3)))
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()].reshape((img.shape))
    imgGRAY = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

    # Try to find chessboard corners (if there's an obstacle it won't be able to do so)
    retIMG, cornersIMG = cv2.findChessboardCorners(imgGRAY, (7,7), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

    return(retIMG)