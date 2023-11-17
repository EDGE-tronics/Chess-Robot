#!/usr/bin/env python
#
# This module copyright 2018, 2022 Richard Day, chess@gotobiz.co.uk
# This code must not be resold, or redistributed in any way without express permission

import sys    
from subprocess import call                         

import time     # import the time library for the sleep function
from math import sin, cos, atan2, sqrt, atan

import serial
serialport = "COM8"  
axistorow8 = 110  # mm
servoonleft = True
squaresize = 32 # mm
gripperfloatheight = 75
grippergrabheight = -20 
gripperoffset = 26
openamount = 37 #degrees
closeamount = 2 #degrees
graveyard = "i6"
msgcount = 0

xmtrans = {
    "a": 3.5,
    "b": 2.5,
    "c": 1.5,
    "d": 0.5,
    "e": -0.5,
    "f": -1.5,
    "g": -2.5,
    "h": -3.5,
    "i": -4.5,
    "j": -5.5
}

xtrans = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9
}
#pieceheights = {
#   "p": 3.2,   # cm
#   "r": 3.6,
#   "n": 3.2,   # grab lower
#   "b": 4.9,
#   "q": 5.7,
#   "k": 6.3
#}
pieceheights = {
    "p": 2.7,   # cm
    "r": 3.0,
    "n": 3.2,   # grab lower
    "b": 4.1,   # 
    "q": 4.6,   # 
    "k": 5.3    # grab lower
}
maxpieceheight = 2.5    # inches

piecewidths = {
    "p": 0,     # degrees
    "r": 3,
    "n": 0,
    "b": 3,
    "q": 4,
    "k": 4
}

gameresult = ("No result", "Checkmate! White wins", "Checkmate! Black wins", "Stalemate", "50 moves rule", "3 repetitions rule")
lastmovetype = (
    "Normal",
    "En passant available",
    "Capture en passant",
    "Pawn promoted",
    "Castle on king's side",
    "Castle on queen's side")

firsttime = 1

sp = 0
SCARA = False

def waiter(dur):
    time.sleep(dur)
    
def receivemsg(sp):
    global msgcount
    msgcount += 1
    #line=sp.readline().decode('utf-8').rstrip()
    line=sp.read_until().decode('utf-8').rstrip()
    sp.flush()
    print(msgcount, line)
    
def scaraviastraight(xmm, adjymmint, zmm):
    global elbow, oldelbow
    #print ("elbow: " + str(elbow) + " oldelbow: " + str(oldelbow))
    oldelbow = elbow
    #print ("elbow: " + str(elbow) + " oldelbow: " + str(oldelbow))
    if xmm > 0 and adjymmint < totalarmlength:
        elbow = 0
    
    if xmm > 135:   # parked
        elbow = 0
    
    if xmm < 0 and adjymmint < totalarmlength:
        elbow = 1

    if elbow != oldelbow:
        print ("elbow: " + str(elbow) + " oldelbow: " + str(oldelbow))
        #intermediate move to straight out
        gstring = "G1" + " X0" + " Y" + str(totalarmlength) + " Z" + str(zmm) + "\r"
        print (gstring)
        sp.write(gstring.encode())
        receivemsg(sp)
        #input("press enter")

def movearmcoord (xmm, ymm, zmm):  # zmm is height
    adjymmint = int(ymm)+axistorow8
    adjxmm = str(int(round(int(xmm))))
    adjymm = str(int(round(int(adjymmint))))
    
    gstring = "G1" + " X" + adjxmm + " Y" + adjymm + " Z" + str(zmm) + "\r"
    print (gstring) ###
    #receivemsg(sp) ####
    #input("Check G-codes then press enter") ###
    sp.flush()
    sp.reset_input_buffer()
    sp.write(gstring.encode())
    receivemsg(sp)
    #receivemsg(sp) ####
    #input("press enter")

def opengripper(amount):
    # adjamount = amount
    # if servoonleft:
        # adjamount = 90 - amount
    # mycode = "M5 T" + str(adjamount) + "\r"
    mycode = "M5\r"
    print ("Open gripper")
    sp.flush()
    sp.write(mycode.encode())
    receivemsg(sp)
    waiter(0.5)

def closegripper(amount, piecetype):
    # adjamount = amount + piecewidths[piecetype]
    # if servoonleft:
        # adjamount = 90 - (adjamount)
    # mycode = "M3 T" + str(adjamount) + "\r"
    mycode = "M3\r"

    print ("Close gripper")
    sp.flush()
    sp.write(mycode.encode())
    receivemsg(sp)
    waiter(0.5)
   
def quitter():
    global sp
    if sp:
        if SCARA:
            gohome()
        print ("reset all steppers")
        sp.flush()
        sp.write(("M18" + "\r").encode())
        receivemsg(sp)
        sp.close()               
    sys.exit()
    #quit()

def pickuppiece(xmm, ymm, piecetype):
    global pieceheights
    opengripper(openamount)
    print("go down to pick up")
    movearmcoord (xmm, ymm, gripperfloatheight)  # go down half way

    waiter(1)
    print ("grippergrabheight:",grippergrabheight)
    movearmcoord (xmm, ymm, grippergrabheight) # go down
    closegripper(closeamount, piecetype)
    #waiter(1)
    print("go up")
    #movearmcoord (xmm, ymm, halfway)
    movearmcoord (xmm, ymm, gripperfloatheight) # go up
    
def droppiece(xmm, ymm):
    
    print("go down to drop piece")
    #movearmcoord (xmm, ymm, halfway)
    movearmcoord (xmm, ymm, grippergrabheight + 2)  # go down
    waiter(1.2)
    opengripper(openamount)
    #waiter(1)
    print("go up")
    #movearmcoord (xmm, ymm, halfway)
    movearmcoord (xmm, ymm, gripperfloatheight) # go up
    
def takepiece (xmm, ymm, targetpiece):
    speaker("Take piece.")
    movearmcoord (xmm, ymm, gripperfloatheight)
    pickuppiece(xmm,ymm, targetpiece)
    gravex = (xmtrans[graveyard[0]] * squaresize)-20
    gravey = (8-int(graveyard[1])) * squaresize
    movearmcoord (gravex, gravey, gripperfloatheight)
    droppiece(gravex, gravey)
    #input("press enter")
    #interx = xmtrans["h"] * squaresize
    #intery = (8-int("3")) * squaresize
    #movearmcoord (interx, intery, gripperfloatheight)
    #input("press enter")
    gohome()


def updateboard(source, target, boardbefore):
    # called from CBint
    sourcex = xtrans[source[0]]
    sourcey = 8-int(source[1])
    targetx = xtrans[target[0]]
    targety = 8-int(target[1])
    print (boardbefore)
    boardbefore[targety][targetx] = boardbefore[sourcey][sourcex] 
    boardbefore[sourcey][sourcex] = "." 
    print (boardbefore) 
    return (boardbefore)

def movepiece (sourcesquarename, targetsquarename, boardbefore):
    # called from CBint 
    sourcexmm = xmtrans[sourcesquarename[0:1]] * squaresize
    sourceymm = (8 - int(sourcesquarename[1:2])) * squaresize
    
    targetxmm = xmtrans[targetsquarename[0:1]] * squaresize
    targetymm = (8 - int(targetsquarename[1:2])) * squaresize
    
    # for board:
    sourcex = xtrans[sourcesquarename[0]]
    sourcey = 8-int(sourcesquarename[1])
    targetx = xtrans[targetsquarename[0]]
    targety = 8-int(targetsquarename[1])
    
    if boardbefore[targety][targetx] != ".":        # row, column
        #print (boardbefore)
        print("Take piece!")
        takepiece(targetxmm, targetymm, boardbefore[targety][targetx].lower())      
    print ("sourcex= ", sourcex)
    
    movearmcoord (sourcexmm, sourceymm, gripperfloatheight)
    sourcepiece = boardbefore[sourcey][sourcex].lower()
    print("sourcepiece " + sourcepiece)

    pickuppiece(sourcexmm, sourceymm, sourcepiece)
    #input("now move piece to target. Enter:")
    movearmcoord (targetxmm, targetymm, gripperfloatheight)

    droppiece(targetxmm, targetymm) 
    print("go home")
    gohome()
    
    iscastling(sourcesquarename)
    enpassant (targetxmm, targetymm) 

def calibrategripper():
    while True:
        angle = input("Provide angle in degrees, or q:")
        if angle == "q":
            quitter()
        opengripper(angle)
        #waiter(1)
def gohome():
    movearmcoord (180, 0, gripperfloatheight)

def initsteppers():
    time.sleep(0.2)
    sp.write(("G28" + "\r").encode())   # steppers off, initialize
    time.sleep(0.2)
    receivemsg(sp)
    time.sleep(0.2)
    receivemsg(sp)
    
def steppers_on():
    sp.write(("M17" + "\r").encode())   # Switch on steppers
    time.sleep(0.2)
    receivemsg(sp)
    time.sleep(0.2)
    receivemsg(sp)
def init():
    global sp
    try:
        sp = serial.Serial(serialport, 115200, timeout=2.0)
        sp.reset_input_buffer()                
    except serial.SerialException as e:
        print("No serial port")
        print (e)
        quitter()
    time.sleep(0.2)
    
    try:
        print ("Start")        
        receivemsg(sp)
        receivemsg(sp)
        print ("Calibrating robot now ...")
        initsteppers()   # turn steppers off and initialize them
        steppers_on()    # prompt user to switch on steppers

        if SCARA:
            gohome()   # raises arm
            gstring = "G1" + " X0" + " Y" + str(totalarmlength) + " Z" + str(gripperfloatheight) + "\r"
            sp.write(gstring.encode())
            receivemsg(sp)
        else:
            movearmcoord (0, (squaresize*3.5), grippergrabheight)
        print("Adjust robot position slightly if not in centre of board.")
        time.sleep(2)
        gohome()

                      
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        quitter()   
    

#init()  # testing
