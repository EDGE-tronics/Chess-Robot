# from picamera.array import PiRGBArray
# from picamera import PiCamera
import cv2
import numpy as np
import string
import time

def findTransformation(img,cbPattern):

    patternSize = (7,7)
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    retCB, cornersCB = cv2.findChessboardCorners(cbPattern, patternSize, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    retIMG, cornersIMG = cv2.findChessboardCorners(imgGray, patternSize, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    
    if retIMG == 0:
        print("Couldn't find chessboard, please adjust your camera and remove any chess piece")
        H = 0
    else:
        H, _ = cv2.findHomography(cornersIMG, cornersCB)     # Find the transformation matrix
    
    return(retIMG, H)

def calibrateCam(cam,type):

    input("Please place the chessboard without the chess pieces and press key")
    cbPattern = cv2.imread('../cb_pattern.jpg', cv2.IMREAD_GRAYSCALE)
    
    # Allow the camera to warmup
    if type == 0:                   # Raspberry Camera module
        rawCapture = PiRGBArray(cam, size=(640, 480))
        time.sleep(0.2)
    elif type == 1:                 # USB Camera
        _, img = cam.read()
        time.sleep(2)

    # Check video frames until the algorithm finds the chessboard corners
    retIMG = 0
    while(retIMG == 0):
        if type == 0:                   # Raspberry Camera module
            cam.capture(rawCapture, format="bgr")
            img = rawCapture.array
            rawCapture.truncate(0)      # Clear the stream in preparation for the next image
        elif type == 1:
            img = cam.read()
        cv2.imshow('Calibration', img)
        cv2.waitKey(1)
        retIMG, H = findTransformation(img,cbPattern)

    cv2.destroyAllWindows()
    print("\nCamera calibration succesful\n")

    warpIMG = cv2.warpPerspective(img, H, (400, 400))

    return(warpIMG, H)

def drawQuadrants(img):

    # Draw quadrants and numbers on image
    imgquad = img.copy()
    cv2.line(imgquad, (200, 0), (200, 400), (255,255,255), 3)
    cv2.line(imgquad, (0, 200), (400, 200), (255,255,255), 3)
    imgquad = cv2.putText(imgquad, '1', (80, 120) , cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA)
    imgquad = cv2.putText(imgquad, '2', (280, 120) , cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA) 
    imgquad = cv2.putText(imgquad, '3', (280, 320) , cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA) 
    imgquad = cv2.putText(imgquad, '4', (80, 320) , cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3, cv2.LINE_AA) 
    cv2.imshow('Quadrants', imgquad)
    cv2.waitKey()
    cv2.destroyAllWindows()

def findWhite(cam,type,H):

    input("Please place the chess pieces and press key")
    cv2.waitKey()

    # Get frame
    if type == 0:                   # Raspberry Camera module
        rawCapture = PiRGBArray(cam, size=(640, 480))
        cam.capture(rawCapture, format="bgr")
        img = rawCapture.array
        time.sleep(1)
    elif type == 1:                 # USB Camera
        img = cam.read()
        time.sleep(7)
    
    # Apply homography transformation
    warpIMG = cv2.warpPerspective(img, H, (400, 400))

    # Draw quedrants and numbers on image
    drawQuadrants(warpIMG)

    return(warpIMG)

def findRotation():

    theta = valid = 0
    while valid == 0:
        print("\nSelect the quadrants where the white pieces are:\n")
        num1 = int(input("First quadrant: ")) 
        num2 = int(input("Second quadrant: "))

        if (num1 == 1 and num2 == 2) or (num1 == 2 and num2 == 1):
            theta = 90
            valid = 1
        elif (num1 == 2 and num2 == 3) or (num1 == 3 and num2 == 2):
            theta = 180
            valid = 1
        elif (num1 == 3 and num2 == 4) or (num1 == 4 and num2 == 3):
            theta = -90
            valid = 1
        elif (num1 == 4 and num2 == 1) or (num1 == 1 and num2 == 4):
            theta = 0
            valid = 1
        if valid == 0:
            print("Please select valid quadrants\n")

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

    # Print results (For testing)
    print("Largest color difference between images:")
    print(largest)
    print("All coordinates:")
    print(coordinates)

    # Make threshold with a percentage of the change in color of the biggest two
    thresh = (largest[0]+largest[1])/2*(0.5)
    for t in range(3,1,-1):
        if largest[t] < thresh:
            coordinates.pop()

    # Print results (For testing)
    print("Moves:")
    print(coordinates)
    
    return(coordinates)

def safetoMove(H):
    #cap = cv2.VideoCapture(1)
    ret, img = cap.read()
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