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
        print("Couldn't find chessboard, please remove any chess piece")
        H = 0
    else:
        # Find homography matrix
        H, _ = cv2.findHomography(cornersIMG, cornersCB)
    
    return(retIMG, H)

def calibrateCam(cam):

    input("Please place the chessboard without the chess pieces and press key")

    # # Allow the camera to warmup and adjust lightning
    img = cam.read()
    time.sleep(7)

    # Check video frames until the algorithm finds the chessboard corners
    retIMG = 0
    while(retIMG == 0):
        ret, img = cam.read()
        if ret:
            retIMG, H = findTransformation(img)

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

def findWhite(cam, H):

    input("Please place the chess pieces and press key")
    cv2.waitKey()

    # Get frame
    ret, frame = cam.read()
    assert ret, "Couldn't take picture"

    # Apply homography transformation
    warpIMG = cv2.warpPerspective(frame, H, (400, 400))

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