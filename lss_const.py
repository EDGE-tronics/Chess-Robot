###############################################################################
#	Author:			Sebastien Parent-Charette (support@robotshop.com)
#	Version:		1.0.0
#	Licence:		LGPL-3.0 (GNU Lesser General Public License version 3)
#	
#	Desscription:	A library that makes using the LSS simple.
#					Offers support for most Python platforms.
#					Uses the Python serial library (pySerial).
###############################################################################

### List of constants

# Bus communication
LSS_DefaultBaud = 115200
LSS_MaxTotalCommandLength = (30 + 1)	# ex: #999XXXX-2147483648\r Adding 1 for end string char (\0)
#										# ex: #999XX000000000000000000\r
LSS_Timeout = 100						# in ms
LSS_CommandStart = "#"
LSS_CommandReplyStart = "*"
LSS_CommandEnd = "\r"
LSS_FirstPositionDisabled = "DIS"

# LSS constants
LSS_ID_Default = 0
LSS_ID_Min = 0
LSS_ID_Max = 250
LSS_Mode255ID = 255
LSS_BroadcastID = 254

# Read/write status
LSS_CommStatus_Idle = 0
LSS_CommStatus_ReadSuccess = 1
LSS_CommStatus_ReadTimeout = 2
LSS_CommStatus_ReadWrongID = 3
LSS_CommStatus_ReadWrongIdentifier = 4
LSS_CommStatus_ReadWrongFormat = 5
LSS_CommStatus_ReadNoBus = 6
LSS_CommStatus_ReadUnknown = 7
LSS_CommStatus_WriteSuccess = 8
LSS_CommStatus_WriteNoBus = 9
LSS_CommStatus_WriteUnknown = 10

# LSS status
LSS_StatusUnknown = 0
LSS_StatusLimp = 1
LSS_StatusFreeMoving = 2
LSS_StatusAccelerating = 3
LSS_StatusTravelling = 4
LSS_StatusDecelerating = 5
LSS_StatusHolding = 6
LSS_StatusOutsideLimits = 7
LSS_StatusStuck = 8				#cannot move at current speed setting
LSS_StatusBlocked = 9			#same as stuck but reached maximum duty and still can't move
LSS_StatusSafeMode = 10
LSS_StatusLast = 11

# LSS models
LSS_ModelHighTorque = 0
LSS_ModelStandard = 1
LSS_ModelHighSpeed = 2
LSS_ModelUnknown = 3

LSS_ModelHT1 = "LSS-HT1"
LSS_ModelST1 = "LSS-ST1"
LSS_ModelHS1 = "LSS-HS1"

# Parameter for query
LSS_QuerySession = 0
LSS_QueryConfig = 1
LSS_QueryInstantaneousSpeed = 2
LSS_QueryTargetTravelSpeed = 3

# Parameter for setter
LSS_SetSession = 0
LSS_SetConfig = 1

# Parameter for Serial/RC mode change
LSS_ModeSerial = 0
LSS_ModePositionRC = 1
LSS_ModeWheelRC = 2

# Parameter for gyre direction
LSS_GyreClockwise = 1
LSS_GyreCounterClockwise = -1

# LED colors
LSS_LED_Black = 0
LSS_LED_Red = 1
LSS_LED_Green = 2
LSS_LED_Blue = 3
LSS_LED_Yellow = 4
LSS_LED_Cyan = 5
LSS_LED_Magenta = 6
LSS_LED_White = 7

# Commands - actions
LSS_ActionReset = "RESET"
LSS_ActionConfirm = "CONFIRM"
LSS_ActionLimp = "L"
LSS_ActionHold = "H"
LSS_ActionParameterTime = "T"
LSS_ActionParameterSpeed = "S"
LSS_ActionMove = "D"
LSS_ActionMoveRelative = "MD"
LSS_ActionWheel = "WD"
LSS_ActionWheelRPM = "WR"

# Commands - actions settings
LSS_ActionOriginOffset = "O"
LSS_ActionAngularRange = "AR"
LSS_ActionMaxSpeed = "SD"
LSS_ActionMaxSpeedRPM = "SR"
LSS_ActionColorLED = "LED"
LSS_ActionGyreDirection = "G"

# Commands - modifiers
LSS_ModifierCurrentHaltHold = "CH"
LSS_ModifierCurrentLimp = "CL"

# Commands - actions advanced settings
LSS_ActionAngularStiffness = "AS"
LSS_ActionAngularHoldingStiffness = "AH"
LSS_ActionAngularAcceleration = "AA"
LSS_ActionAngularDeceleration = "AD"
LSS_ActionEnableMotionControl = "EM"

# Commands - queries
LSS_QueryStatus = "Q"
LSS_QueryOriginOffset = "QO"
LSS_QueryAngularRange = "QAR"
LSS_QueryPositionPulse = "QP"
LSS_QueryPosition = "QD"
LSS_QuerySpeed = "QWD"
LSS_QuerySpeedRPM = "QWR"
LSS_QuerySpeedPulse = "QS"
LSS_QueryMaxSpeed = "QSD"
LSS_QueryMaxSpeedRPM = "QSR"
LSS_QueryColorLED = "QLED"
LSS_QueryGyre = "QG"
LSS_QueryID = "QID"
LSS_QueryBaud = "QB"
LSS_QueryFirstPosition = "QFD"
LSS_QueryModelString = "QMS"
LSS_QuerySerialNumber = "QN"
LSS_QueryFirmwareVersion = "QF"
LSS_QueryVoltage = "QV"
LSS_QueryTemperature = "QT"
LSS_QueryCurrent = "QC"

# Commands - queries advanced
LSS_QueryAngularStiffness = "QAS"
LSS_QueryAngularHoldingStiffness = "QAH"
LSS_QueryAngularAcceleration = "QAA"
LSS_QueryAngularDeceleration = "QAD"
LSS_QueryEnableMotionControl = "QEM"
LSS_QueryBlinkingLED = "QLB"

# Commands - configurations
LSS_ConfigID = "CID"
LSS_ConfigBaud = "CB"
LSS_ConfigOriginOffset = "CO"
LSS_ConfigAngularRange = "CAR"
LSS_ConfigMaxSpeed = "CSD"
LSS_ConfigMaxSpeedRPM = "CSR"
LSS_ConfigColorLED = "CLED"
LSS_ConfigGyreDirection = "CG"
LSS_ConfigFirstPosition = "CFD"
LSS_ConfigMode = "CRC"

# Commands - configurations advanced
LSS_ConfigAngularStiffness = "CAS"
LSS_ConfigAngularHoldingStiffness = "CAH"
LSS_ConfigAngularAcceleration = "CAA"
LSS_ConfigAngularDeceleration = "CAD"
LSS_ConfigBlinkingLED = "CLB"

### EOF #######################################################################
