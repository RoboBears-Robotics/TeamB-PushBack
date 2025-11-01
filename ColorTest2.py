#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
# AI Vision Color Descriptions
ai_vision_21__RedBlock = Colordesc(1, 195, 74, 119, 13, 0.91)
ai_vision_21__BlueBlock = Colordesc(2, 41, 100, 159, 8, 0.27)
# AI Vision Code Descriptions
ai_vision_21 = AiVision(Ports.PORT21, ai_vision_21__RedBlock, ai_vision_21__BlueBlock)
FrontLandM = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
TopMotors = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
BackMiddle = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
BackLower = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

ai_vision_1_objects = []
screen_precision = 0
console_precision = 0
myVariable = 0

buttonXActive = False
buttonBActive = False
buttonUpActive = False
buttonLRActive = False
buttonDownActive = False

def buttonBFunct():
    BackMiddle.stop()
    TopMotors.stop()
    FrontLandM.stop()
    BackLower.stop()
    global buttonBActive
    if not buttonBActive:
        FrontLandM.spin(FORWARD)
        BackLower.spin(REVERSE)
        buttonBActive = True
    else:
        buttonBActive = False

def buttonXFunct():
    BackMiddle.stop()
    TopMotors.stop()
    FrontLandM.stop()
    BackLower.stop()
    global buttonXActive
    if not buttonXActive:
        FrontLandM.spin(FORWARD)
        BackLower.spin(FORWARD)
        BackMiddle.spin(REVERSE)
        buttonXActive = True
    else:
        buttonXActive = False

def buttonUpFunct():
    BackMiddle.stop()
    TopMotors.stop()
    FrontLandM.stop()
    BackLower.stop()
    global buttonUpActive
    if not buttonUpActive:
        FrontLandM.spin(FORWARD)
        BackLower.spin(REVERSE)
        TopMotors.spin(FORWARD)
        BackMiddle.spin(FORWARD)
        buttonUpActive = True
    else:
        buttonUpActive = False

def buttonLRFunct():
    BackMiddle.stop()
    TopMotors.stop()
    FrontLandM.stop()
    BackLower.stop()
    global buttonLRActive
    if not buttonLRActive:
        FrontLandM.spin(FORWARD)
        BackLower.spin(REVERSE)
        BackMiddle.spin(FORWARD)
        TopMotors.spin(REVERSE)
        buttonLRActive = True
    else:
        buttonLRActive = False

def buttonDownFunct():
    BackMiddle.stop()
    TopMotors.stop()
    FrontLandM.stop()
    BackLower.stop()
    global buttonDownActive
    if not buttonDownActive:
        FrontLandM.spin(REVERSE)
        BackMiddle.spin(FORWARD)
        BackLower.spin(REVERSE)
        buttonDownActive = True
    else:
        buttonDownActive = False

controller_1.buttonX.pressed(buttonXFunct)
controller_1.buttonB.pressed(buttonBFunct)
controller_1.buttonUp.pressed(buttonUpFunct)
controller_1.buttonLeft.pressed(buttonLRFunct)
controller_1.buttonRight.pressed(buttonLRFunct)
controller_1.buttonDown.pressed(buttonDownFunct)

def checkBlue():
    global myVariable, ai_vision_1_objects, screen_precision, console_precision
    brain.screen.set_font(FontType.MONO40)
    brain.screen.clear_row(1)
    brain.screen.set_cursor(brain.screen.row(), 1)
    brain.screen.set_cursor(1, 1)
    ai_vision_1_objects = ai_vision_21.take_snapshot(ai_vision_21__BlueBlock)
    if ai_vision_1_objects and len(ai_vision_1_objects) > 0:
        brain.screen.print("Blue Object Found")
    else:
        brain.screen.print("No Blue Object")

def checkRed():
    global myVariable, ai_vision_1_objects, screen_precision, console_precision
    brain.screen.set_font(FontType.MONO40)
    brain.screen.clear_row(3)
    brain.screen.set_cursor(brain.screen.row(), 1)
    brain.screen.set_cursor(3, 1)
    ai_vision_1_objects = ai_vision_21.take_snapshot(ai_vision_21__RedBlock)
    if ai_vision_1_objects and len(ai_vision_1_objects) > 0:
        brain.screen.print("Red Object Found")
    else:
        brain.screen.print("No Red Object")

def pre_autonomous():
    # actions to do when the program starts
    brain.screen.clear_screen()
    brain.screen.print("pre auton code")
    wait(1, SECONDS)

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():
    # global myVariable, ai_vision_1_objects, screen_precision, console_precision
    # while True:
        # checkBlue()
        # checkRed()
        # wait(0.1, SECONDS)
        # wait(20, MSEC)
    pass
    
comp = Competition(user_control, autonomous)
pre_autonomous()
