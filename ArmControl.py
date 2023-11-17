import numpy as np
from math import atan2, sqrt, cos, sin, acos, pi, copysign
import time
import os
# from gtts import gTTS
import VisionModule as vm
# import platform
# import Interface as inter
import mat_robot_move as mrm


mrm.init()


def CBtoXY(targetCBsq, params, color):

    wletterWeight = [-4, -3, -2, -1, 0, 1, 2, 3]
    bletterWeight = [3, 2, 1, 0, -1, -2, -3, -4]
    bnumberWeight = [8, 7, 6, 5, 4, 3, 2, 1]
    if targetCBsq[0] == 'k':
        #x = 6 * params["sqSize"]
        #y = 6 * params["sqSize"]
        x = 6 * mrm.squaresize
        y = 6 * mrm.squaresize
    else:
        if color:         # White -> Robot color = Black
            sqletter = bletterWeight[ord(targetCBsq[0]) -97]
            sqNumber = bnumberWeight[int(targetCBsq[1]) - 1]
        else:             # Black
            sqletter = wletterWeight[ord(targetCBsq[0]) -97]
            sqNumber = int(targetCBsq[1])

        y=sqNumber * mrm.squaresize - (mrm.squaresize)
        x=sqletter * mrm.squaresize + (mrm.squaresize/2)

    return(x,y)

def executeMove(move, params, color, homography, cap, selectedCam):

#    allMotors.setColorLED(lssc.LSS_LED_Cyan)
    z = params["cbHeight"] + params["pieceHeight"]
    angles_rest = (0,-1155,450,1050,0)
    gClose = -2
    gOpen = -9.5
    goDown = 0.6*params["pieceHeight"]
    gripState = gOpen
    x, y = 0, 0
    
    for i in range(0,len(move),2):

        # Calculate position and FPC
        x0, y0 = x, y
        x, y = CBtoXY((move[i],move[i+1]), params, color)                
        print("Input: move[i],move[i+1]", move[i],move[i+1])
        print("Result: x,y,x0,y0",x,y,x0,y0)
        
        mrm.movearmcoord(x,y,mrm.gripperfloatheight)

        if (i/2)%2: # Uneven move (go lower to grab the piece)
            #gripState = gOpen
            #goDown = 0.6*params["pieceHeight"]
            mrm.droppiece(x,y)
            
        else:       # Even move (go a little higher to drop the piece)
            #gripState = gClose
            #goDown = 0.5*params["pieceHeight"]
            mrm.pickuppiece(x,y,'b')

    mrm.gohome()       
    moveState =1
  

    time.sleep(4)
    return(moveState)

