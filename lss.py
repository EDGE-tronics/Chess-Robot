###############################################################################
#	Author:			Sebastien Parent-Charette (support@robotshop.com)
#	Version:		1.0.0
#	Licence:		LGPL-3.0 (GNU Lesser General Public License version 3)
#	
#	Desscription:	A library that makes using the LSS simple.
#					Offers support for most Python platforms.
#					Uses the Python serial library (pySerial).
###############################################################################

### Import required liraries
import re
import serial
from math import sqrt, atan, acos, fabs

### Import constants
import lss_const as lssc

### Class functions
def initBus(portName, portBaud):
	LSS.bus = serial.Serial(portName, portBaud)
	LSS.bus.timeout = 0.1

def closeBus():
	if LSS.bus is not None:
		LSS.bus.close()
		del LSS.bus

# Write with optional parameter and modifiers
def genericWrite(id, cmd, param = None, mod = None, value = None, mod2 = None, val2 = None):
	if LSS.bus is None:
		return False
	if mod is None:
		if param is None:
			LSS.bus.write((lssc.LSS_CommandStart + str(id) + cmd + lssc.LSS_CommandEnd).encode())
		else:
			LSS.bus.write((lssc.LSS_CommandStart + str(id) + cmd + str(param) + lssc.LSS_CommandEnd).encode())
	else:
		if mod2 is None:
			LSS.bus.write((lssc.LSS_CommandStart + str(id) + cmd + str(param) + mod + str(value) + lssc.LSS_CommandEnd).encode())
		else:
			LSS.bus.write((lssc.LSS_CommandStart + str(id) + cmd + str(param) + mod + str(value) + mod2 + str(val2) + lssc.LSS_CommandEnd).encode())
	return True

# Read an integer result
def genericRead_Blocking_int(id, cmd):
	if LSS.bus is None:
		return None
	try:
		# Get start of packet and discard header and everything before
		c = LSS.bus.read()
		while (c.decode("utf-8") != lssc.LSS_CommandReplyStart):
			c = LSS.bus.read()
			if(c.decode("utf-8") == ""):
				break
		# Get packet
		data = LSS.bus.read_until(lssc.LSS_CommandEnd)
		# Parse packet
		matches = re.match("(\d{1,3})([A-Z]{1,4})(-?\d{1,18})", data.decode("utf-8"), re.I)
		# Check if matches are found
		if(matches is None):
			return(None)
		if((matches.group(1) is None) or (matches.group(2) is None) or (matches.group(3) is None)):
			return(None)
		# Get values from match
		readID = matches.group(1)
		readIdent = matches.group(2)
		readValue = matches.group(3)
		# Check id
		if(readID != str(id)):
			return(None)
		# Check identifier
		if(readIdent != cmd):
			return(None)
	except:
		return(None)
	# return value
	return(readValue)

# Read a string result
#@classmethod
def genericRead_Blocking_str(id, cmd, numChars):
	if LSS.bus is None:
		return None
	if LSS.bus is None:
		return None
	try:
		# Get start of packet and discard header and everything before
		c = LSS.bus.read()
		while (c.decode("utf-8") != lssc.LSS_CommandReplyStart):
			c = LSS.bus.read()
			if(c.decode("utf-8") == ""):
				break
		# Get packet
		data = LSS.bus.read_until(lssc.LSS_CommandEnd)
		data = (data[:-1])
		# Parse packet
		matches = re.match("(\d{1,3})([A-Z]{1,4})(.{" + str(numChars) + "})", data.decode("utf-8"), re.I)
		# Check if matches are found
		if(matches is None):
			return(None)
		if((matches.group(1) is None) or (matches.group(2) is None) or (matches.group(3) is None)):
			return(None)
		# Get values from match
		readID = matches.group(1)
		readIdent = matches.group(2)
		readValue = matches.group(3)
		# Check id
		if(readID != str(id)):
			return(None)
		# Check identifier
		if(readIdent != cmd):
			return(None)
	except:
		return(None)
	# return value
	return(readValue)

class LSS:
	# Class attribute
	bus = None
	
	### Constructor
	def __init__(self, id = 0):
		self.servoID = id
	
	### Attributes
	servoID = 0
	
	### Functions
	#> Actions
	def reset(self):
		return (genericWrite(self.servoID, lssc.LSS_ActionReset))

	def confirm(self):
		return (genericWrite(self.servoID, lssc.LSS_ActionConfirm))
	
	def limp(self):
		return (genericWrite(self.servoID, lssc.LSS_ActionLimp))
	
	def hold(self):
		return (genericWrite(self.servoID, lssc.LSS_ActionHold))
	
	def move(self, pos):
		return (genericWrite(self.servoID, lssc.LSS_ActionMove, pos))
	
	def moveRelative(self, delta):
		return (genericWrite(self.servoID, lssc.LSS_ActionMoveRelative, delta))
	
	def wheel(self, speed):
		return (genericWrite(self.servoID, lssc.LSS_ActionWheel, speed))
	
	def wheelRPM(self, rpm):
		return (genericWrite(self.servoID, lssc.LSS_ActionWheelRPM, rpm))

	def moveT(self, pos, value):
		return (genericWrite(self.servoID, lssc.LSS_ActionMove, pos, lssc.LSS_ActionParameterTime, value))
	
	def moveCH(self, pos, value):
		return (genericWrite(self.servoID, lssc.LSS_ActionMove, pos, lssc.LSS_ModifierCurrentHaltHold, value))

	def moveCHT(self, pos, value, tval):
		return (genericWrite(self.servoID, lssc.LSS_ActionMove, pos, lssc.LSS_ModifierCurrentHaltHold, value, lssc.LSS_ActionParameterTime, tval))

	def moveCL(self, pos, value):
		return (genericWrite(self.servoID, lssc.LSS_ActionMove, pos, lssc.LSS_ModifierCurrentLimp, value))
	
	#> Queries
	#def getID(self):
	#def getBaud(self):
	
	def getStatus(self):
		genericWrite(self.servoID, lssc.LSS_QueryStatus)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryStatus))
	
	def getOriginOffset(self, queryType = lssc.LSS_QuerySession):
		genericWrite(self.servoID, lssc.LSS_QueryOriginOffset, queryType)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryOriginOffset))
	
	def getAngularRange(self, queryType = lssc.LSS_QuerySession):
		genericWrite(self.servoID, lssc.LSS_QueryAngularRange, queryType)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryAngularRange))
	
	def getPositionPulse(self):
		genericWrite(self.servoID, lssc.LSS_QueryPositionPulse)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryPositionPulse))
	
	def getPosition(self):
		genericWrite(self.servoID, lssc.LSS_QueryPosition)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryPosition))
	
	def getSpeed(self):
		genericWrite(self.servoID, lssc.LSS_QuerySpeed)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QuerySpeed))
	
	def getSpeedRPM(self):
		genericWrite(self.servoID, lssc.LSS_QuerySpeedRPM)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QuerySpeedRPM))
	
	def getSpeedPulse(self):
		genericWrite(self.servoID, lssc.LSS_QuerySpeedPulse)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QuerySpeedPulse))
	
	def getMaxSpeed(self, queryType = lssc.LSS_QuerySession):
		genericWrite(self.servoID, lssc.LSS_QueryMaxSpeed, queryType)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryMaxSpeed))
	
	def getMaxSpeedRPM(self, queryType = lssc.LSS_QuerySession):
		genericWrite(self.servoID, lssc.LSS_QueryMaxSpeedRPM, queryType)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryMaxSpeedRPM))
	
	def getColorLED(self, queryType = lssc.LSS_QuerySession):
		genericWrite(self.servoID, lssc.LSS_QueryColorLED, queryType)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryColorLED))
	
	def getGyre(self, queryType = lssc.LSS_QuerySession):
		genericWrite(self.servoID, lssc.LSS_QueryGyre, queryType)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryGyre))
	
	# returns 0 if "DIS"
	def getFirstPosition(self):
		genericWrite(self.servoID, lssc.LSS_QueryFirstPosition)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryFirstPosition))
	
	# returns true/false based on if QFD returns "DIS" (= False)
	def getIsFirstPositionEnabled(self):
		genericWrite(self.servoID, lssc.LSS_QueryFirstPosition)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryFirstPosition) is not None)
	
	def getModel(self):
		genericWrite(self.servoID, lssc.LSS_QueryModelString)
		return (genericRead_Blocking_str(self.servoID, lssc.LSS_QueryModelString, 7))
	
	def getSerialNumber(self):
		genericWrite(self.servoID, lssc.LSS_QuerySerialNumber)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QuerySerialNumber))
	
	def getFirmwareVersion(self):
		genericWrite(self.servoID, lssc.LSS_QueryFirmwareVersion)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryFirmwareVersion))
	
	def getVoltage(self):
		genericWrite(self.servoID, lssc.LSS_QueryVoltage)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryVoltage))
	
	def getTemperature(self):
		genericWrite(self.servoID, lssc.LSS_QueryTemperature)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryTemperature))
	
	def getCurrent(self):
		genericWrite(self.servoID, lssc.LSS_QueryCurrent)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryCurrent))
	
	#> Queries (advanced)
	def getAngularStiffness(self, queryType = lssc.LSS_QuerySession):
		genericWrite(self.servoID, lssc.LSS_QueryAngularStiffness, queryType)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryAngularStiffness))
	
	def getAngularHoldingStiffness(self, queryType = lssc.LSS_QuerySession):
		genericWrite(self.servoID, lssc.LSS_QueryAngularHoldingStiffness, queryType)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryAngularHoldingStiffness))
	
	def getAngularAcceleration(self, queryType = lssc.LSS_QuerySession):
		genericWrite(self.servoID, lssc.LSS_QueryAngularAcceleration, queryType)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryAngularAcceleration))
	
	def getAngularDeceleration(self, queryType = lssc.LSS_QuerySession):
		genericWrite(self.servoID, lssc.LSS_QueryAngularDeceleration, queryType)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryAngularDeceleration))
	
	def getIsMotionControlEnabled(self):
		genericWrite(self.servoID, lssc.LSS_QueryEnableMotionControl)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryEnableMotionControl))
	
	def getBlinkingLED(self):
		genericWrite(self.servoID, lssc.LSS_QueryBlinkingLED)
		return (genericRead_Blocking_int(self.servoID, lssc.LSS_QueryBlinkingLED))
	
	#> Configs
	def setOriginOffset(self, pos, setType = lssc.LSS_SetSession):
		if setType == lssc.LSS_SetSession:
			return (genericWrite(self.servoID, lssc.LSS_ActionOriginOffset, pos))
		elif setType == lssc.LSS_SetConfig:
			return (genericWrite(self.servoID, lssc.LSS_ConfigOriginOffset, pos))
	
	def setAngularRange(self, delta, setType = lssc.LSS_SetSession):
		if setType == lssc.LSS_SetSession:
			return (genericWrite(self.servoID, lssc.LSS_ActionAngularRange, delta))
		elif setType == lssc.LSS_SetConfig:
			return (genericWrite(self.servoID, lssc.LSS_ConfigAngularRange, delta))
	
	def setMaxSpeed(self, speed, setType = lssc.LSS_SetSession):
		if setType == lssc.LSS_SetSession:
			return (genericWrite(self.servoID, lssc.LSS_ActionMaxSpeed, speed))
		elif setType == lssc.LSS_SetConfig:
			return (genericWrite(self.servoID, lssc.LSS_ConfigMaxSpeed, speed))
	
	def setMaxSpeedRPM(self, rpm, setType = lssc.LSS_SetSession):
		if setType == lssc.LSS_SetSession:
			return (genericWrite(self.servoID, lssc.LSS_ActionMaxSpeedRPM, rpm))
		elif setType == lssc.LSS_SetConfig:
			return (genericWrite(self.servoID, lssc.LSS_ConfigMaxSpeedRPM, rpm))
	
	def setColorLED(self, color, setType = lssc.LSS_SetSession):
		if setType == lssc.LSS_SetSession:
			return (genericWrite(self.servoID, lssc.LSS_ActionColorLED, color))
		elif setType == lssc.LSS_SetConfig:
			return (genericWrite(self.servoID, lssc.LSS_ConfigColorLED, color))
	
	def setGyre(self, gyre, setType = lssc.LSS_SetSession):
		if setType == lssc.LSS_SetSession:
			return (genericWrite(self.servoID, lssc.LSS_ActionGyreDirection, gyre))
		elif setType == lssc.LSS_SetConfig:
			return (genericWrite(self.servoID, lssc.LSS_ConfigGyreDirection, gyre))
	
	def setFirstPosition(self, pos):
		return (genericWrite(self.servoID, lssc.LSS_ConfigFirstPosition, pos))
	
	def clearFirstPosition(self):
		return (genericWrite(self.servoID, lssc.LSS_ConfigFirstPosition))
	
	def setMode(self, mode):
		return (genericWrite(self.servoID, lssc.LSS_ConfigMode, mode))
	
	#> Configs (advanced)
	def setAngularStiffness(self, value, setType = lssc.LSS_SetSession):
		if setType == lssc.LSS_SetSession:
			return (genericWrite(self.servoID, lssc.LSS_ActionAngularStiffness, value))
		elif setType == lssc.LSS_SetConfig:
			return (genericWrite(self.servoID, lssc.LSS_ConfigAngularStiffness, value))
	
	def setAngularHoldingStiffness(self, value, setType = lssc.LSS_SetSession):
		if setType == lssc.LSS_SetSession:
			return (genericWrite(self.servoID, lssc.LSS_ActionAngularHoldingStiffness, value))
		elif setType == lssc.LSS_SetConfig:
			return (genericWrite(self.servoID, lssc.LSS_ConfigAngularHoldingStiffness, value))
	
	def setAngularAcceleration(self, value, setType = lssc.LSS_SetSession):
		if setType == lssc.LSS_SetSession:
			return (genericWrite(self.servoID, lssc.LSS_ActionAngularAcceleration, value))
		elif setType == lssc.LSS_SetConfig:
			return (genericWrite(self.servoID, lssc.LSS_ConfigAngularAcceleration, value))
	
	def setAngularDeceleration(self, value, setType = lssc.LSS_SetSession):
		if setType == lssc.LSS_SetSession:
			return (genericWrite(self.servoID, lssc.LSS_ActionAngularDeceleration, value))
		elif setType == lssc.LSS_SetConfig:
			return (genericWrite(self.servoID, lssc.LSS_ConfigAngularDeceleration, value))
	
	def setMotionControlEnabled(self, value):
		return (genericWrite(self.servoID, lssc.LSS_ActionEnableMotionControl, value))
	
	def setBlinkingLED(self, state):
		return (genericWrite(self.servoID, lssc.LSS_ConfigBlinkingLED, state))
	
### EOF ######################################################################