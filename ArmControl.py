import numpy as np
from math import atan2, sqrt, cos, sin, acos, pi, copysign
import time
import os
from gtts import gTTS
import VisionModule as vm
import lss
import lss_const as lssc
import platform
import Interface as inter

if platform.system() == 'Windows':
    port = "COM3"
elif platform.system() == 'Linux':
    port = "/dev/ttyUSB0"
    
lss.initBus(port,lssc.LSS_DefaultBaud) 
base = lss.LSS(1)
shoulder = lss.LSS(2)
elbow = lss.LSS(3)
wrist = lss.LSS(4)
gripper = lss.LSS(5)
allMotors = lss.LSS(254)

allMotors.setAngularStiffness(0)
allMotors.setAngularHoldingStiffness(0)
allMotors.setMaxSpeed(60)
wrist.setMaxSpeed(120)

CST_ANGLE_MIN = -90
CST_ANGLE_MAX = 90

def checkConstraints(value, min, max):
    if (value < min):
        value = min
    if (value > max):
        value = max
    return (value)

# Desired positions in x, y, z, gripper aperture
def LSS_IK(targetXYZG):

    d1 = 4.13   # Bottom to shoulder
    d2 = 5.61   # Shoulder to elbow
    d3 = 6.39   # Elbow to wrist
    d4 = 4.52   # Wrist to end of gripper

    x0 = targetXYZG[0]
    y0 = targetXYZG[1]
    z0 = targetXYZG[2]
    g0 = targetXYZG[3]

    # Base angle (degrees)
    q1 = atan2(y0,x0) * 180/pi

    # Radius from the axis of rotation of the base in xy plane
    xyr = sqrt(x0**2 + y0**2)

    # Pitch angle    
    q0 = 80

    # Gripper components in xz plane
    lx = d4 * cos(q0 * pi/180)
    lz = d4 * sin(q0 * pi/180)

    # Wrist coordinates in xz plane
    x1 = xyr - lx
    z1 = z0 + lz - d1

    # Distance between the shoulder axis and the wrist axis
    h = sqrt(x1**2 + z1**2)

    a1 = atan2(z1,x1)
    a2 = acos((d2**2 - d3**2 + h**2)/(2 * d2 * h))

    # Shoulder angle (degrees)
    q2 = (a1 + a2) * 180/pi

    # Elbow angle (degrees)
    a3 = acos((d2**2 + d3**2 - h**2)/(2 * d2 * d3))
    q3 = 180 - a3 * 180/pi

    # Wrist angle (degrees) (add 5 deg because of the wrist-gripper offset)
    q4 = q0 - (q3 - q2) + 5

    #  Add 15 deg because of the shoulder-elbow axis offset
    q2 = q2 + 15

    # Return values Base, Shoulder, Elbow, Wrist, Gripper
    angles_BSEWG = [ q1,   90-q2,   q3-90,  q4,     g0]

    # Check constraints
    for i in range(0,5):
        angles_BSEWG[i] = checkConstraints(angles_BSEWG[i], CST_ANGLE_MIN, CST_ANGLE_MAX)

    return(np.dot(10,angles_BSEWG).astype(int))

def LSSA_moveMotors(angles_BSEWG):

    # If the servos detect a current >= 600mA(gripper)/1A(other servos) before reaching the requested positions they will halt and hold
    wrist.moveCH(angles_BSEWG[3], 1000)
    shoulder.moveCH(angles_BSEWG[1], 1000)
    elbow.moveCH(angles_BSEWG[2], 1000)
    base.moveCH(angles_BSEWG[0], 1000)
    gripper.moveCH(angles_BSEWG[4], 600)

    arrived = False
    issue = False

    # Check if they reached the requested position
    while arrived == False and issue == False:
        bStat = base.getStatus()
        sStat = shoulder.getStatus()
        eStat = elbow.getStatus()
        wStat = wrist.getStatus()
        gStat = gripper.getStatus()
        # If a status is None print message
        if (bStat is None or sStat is None or eStat is None or wStat is None or gStat is None):
            print("- Unknown status")
            arrived = False
        # If the statuses aren't None check their values
        else:
            # If a servo is Outside limits, Stuck, Blocked or in Safe Mode before it reaches the requested position reset the servos and return issue
            if (bStat>'6'  or sStat>'6' or eStat>'6'or wStat>'6' or gStat>'6'):
                allMotors.setColorLED(lssc.LSS_LED_Red)
                allMotors.reset
                time.sleep(2)
                allMotors.confirm
                print("- Issue detected")
                issue = True
            # If all the servos are holding positions check if they have arrived
            elif (bStat=='6' and sStat=='6' and eStat=='6' and wStat=='6' and gStat=='6'):
                bPos = base.getPosition()
                sPos = shoulder.getPosition()
                ePos = elbow.getPosition()
                wPos = wrist.getPosition()
                # If any position is None
                if (bPos is None or sPos is None or ePos is None or wPos is None):
                    print("- Unknown position")
                # If they are holding in a different position than requested one return issue
                elif (abs(int(bPos)-angles_BSEWG[0])>20 or abs(int(sPos)-angles_BSEWG[1])>20 or abs(int(ePos)-angles_BSEWG[2])>20 or abs(int(wPos)-angles_BSEWG[3])>20):
                    # Debugging
                    print("Base Current (mA) = " + str(base.getCurrent()))
                    print("Shoulder Current (mA) = " + str(shoulder.getCurrent()))
                    print("Elbow Current (mA) = " + str(elbow.getCurrent()))
                    print("Wrist Current (mA) = " + str(wrist.getCurrent()))

                    print("- Obstacle detected")
                    issue = True
                else:
                    print("- Arrived\n")
                    arrived = True

    return(arrived)

def CBtoXY(targetCBsq, params):
    global playerColor

    wletterWeight = [-4, -3, -2, -1, 1, 2, 3, 4]
    bletterWeight = [4, 3, 2, 1, -1, -2, -3, -4]
    bnumberWeight = [8, 7, 6, 5, 4, 3, 2, 1]

    if targetCBsq[0] == 'k':
        x = 6 * params["sqSize"]
        y = 6 * params["sqSize"]
    else:
        if playerColor:         # White -> Robot color = Black
            sqletter = bletterWeight[ord(targetCBsq[0]) - 97]
            sqNumber = bnumberWeight[int(targetCBsq[1]) - 1]
        else:                   # Black
            sqletter = wletterWeight[ord(targetCBsq[0]) - 97]
            sqNumber = int(targetCBsq[1])

        x = params["baseradius"] + params["cbFrame"] + params["sqSize"] * sqNumber - params["sqSize"]*1/2
        y = params["sqSize"] * sqletter - copysign(params["sqSize"]*1/2,sqletter)

    return(x,y)

def executeMove(move, params, color, homography, cap):
    global playerColor

    moveState = False
    playerColor = color
    allMotors.setColorLED(lssc.LSS_LED_Cyan)
    z = params["cbHeight"] + params["pieceHeight"]
    angles_rest = (0,-1100,450,1100,0)
    gClose = -1.5
    gOpen = -8
    goDown = 0.6*params["pieceHeight"]
    gripState = gOpen
    
    for i in range(0,len(move),2):

        # Move to position (up)
        x, y = CBtoXY((move[i],move[i+1]), params)
        angles_BSEWG1 = LSS_IK([x, y, z + 1, gripState])
        print("1) MOVE UP")
        arrived1 = LSSA_moveMotors(angles_BSEWG1)
        askPermision(angles_BSEWG1, arrived1, homography, cap)

        # Go down
        angles_BSEWG2 = LSS_IK([x, y, z - 1 - goDown, gripState])
        print("2) GO DOWN")
        arrived2 = LSSA_moveMotors(angles_BSEWG2)
        askPermision(angles_BSEWG2, arrived2, homography, cap)

        if (i/2)%2: # Uneven move (go lower to grab the piece)
            gripState = gOpen
            goDown = 0.6*params["pieceHeight"]
        else:       # Even move (go a little higher to drop the piece)
            gripState = gClose
            goDown = 0.5*params["pieceHeight"]

        # Close / Open the gripper
        gripper.moveCH(int(gripState*10), 600)
        time.sleep(1)
        print("3) CLOSE/OPEN the gripper\n")
        
        # Go up
        angles_BSEWG3 = LSS_IK([x, y, z + 1, gripState])
        print("4) GO UP")
        arrived3 = LSSA_moveMotors(angles_BSEWG3)
        askPermision(angles_BSEWG3, arrived3, homography, cap)

    # Go back to resting position and go limp
    print("5) REST")
    _ = LSSA_moveMotors(angles_rest)
    time.sleep(2)
    allMotors.limp()
    allMotors.setColorLED(lssc.LSS_LED_Black)

    return(moveState)

def askPermision(angles_BSEWG, arrived, homography, cap):

    angles_rest = (0,-1100,450,1100,0)
    sec = 0

    while arrived == False:                                 # If the servos couldn't reach the requested position
        if sec == 0:
            inter.speak("excuse")                           # Play audio asking for permission
            pass
        else:
            pass
            inter.speak("please")
        allMotors.setColorLED(lssc.LSS_LED_Magenta)         # Change LEDs to Magenta
        _ = LSSA_moveMotors(angles_rest)                    # Go to resting position
        allMotors.limp()
        sec = 0

        while arrived == False and sec < 5:                 # If the servos couldn't reach the requested position and we haven't waited 5 sec
            if vm.safetoMove(homography, cap) != 0 or sec == 4:  # We check if it is safe to move (vision code) or if we have waited 5 sec
                allMotors.setColorLED(lssc.LSS_LED_Cyan)    # If it is true we change LEDs back to cyan
                arrived = LSSA_moveMotors(angles_BSEWG)     # And try moving the motors again
            else:
                time.sleep(1)                               # Wait one second
            sec = sec + 1

def winLED(allMotors):
    for i in range (0, 4):
        for j in range (1, 8):                  # Loop through each of the 8 LED color (black = 0, red = 1, ..., white = 7)
            allMotors.setColorLED(j)            # Set the color (session) of the LSS
            time.sleep(0.3)                     # Wait 0.3 seconds per color change
    allMotors.setColorLED(lssc.LSS_LED_Black)