#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
# AI Vision Color Descriptions
ai_vision_1__RedBlock = Colordesc(1, 195, 74, 119, 13, 0.91)
ai_vision_1__BlueBlock = Colordesc(2, 41, 100, 159, 8, 0.27)
# AI Vision Code Descriptions
ai_vision_1 = AiVision(Ports.PORT1, ai_vision_1__RedBlock, ai_vision_1__BlueBlock)


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

# Motor Function Definitions

def FrontLMForward():
    if FrontLandM.is_spinning():
        FrontLandM.stop()
    else:
        FrontLandM.spin(FORWARD)

def FrontLMReverse():
    if FrontLandM.is_spinning():
        FrontLandM.stop()
    else:
        FrontLandM.spin(REVERSE)

def TopMotorForward():
    if TopMotors.is_spinning():
        TopMotors.stop()
    else:
        TopMotors.spin(FORWARD)

def TopMotorReverse():
    if TopMotors.is_spinning():
        TopMotors.stop()
    else:
        TopMotors.spin(REVERSE)

def BackMiddleForward():
    if BackMiddle.is_spinning():
        BackMiddle.stop()
    else:
        BackMiddle.spin(FORWARD)

def BackMiddleReverse():
    if BackMiddle.is_spinning():
        BackMiddle.stop()
    else:
        BackMiddle.spin(REVERSE)

def BackLowerForward():
    if BackLower.is_spinning():
        BackLower.stop()
    else:
        BackLower.spin(FORWARD)

def BackLowerReverse():
    if BackLower.is_spinning():
        BackLower.stop()
    else:
        BackLower.spin(REVERSE)

TopMotors.set_velocity(100, PERCENT)
FrontLandM.set_velocity(100, PERCENT)
BackMiddle.set_velocity(100, PERCENT)
BackLower.set_velocity(100, PERCENT)

# Color Sorting Functions

ai_vision_1_objects = []
screen_precision = 0
console_precision = 0
myVariable = 0

def checkBlue():
    global myVariable, ai_vision_1_objects, screen_precision, console_precision
    brain.screen.set_font(FontType.MONO40)
    brain.screen.clear_row(1)
    brain.screen.set_cursor(brain.screen.row(), 1)
    brain.screen.set_cursor(1, 1)
    ai_vision_1_objects = ai_vision_1.take_snapshot(ai_vision_1__BlueBlock)
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
    ai_vision_1_objects = ai_vision_1.take_snapshot(ai_vision_1__RedBlock)
    if ai_vision_1_objects and len(ai_vision_1_objects) > 0:
        brain.screen.print("Red Object Found")
    else:
        brain.screen.print("No Red Object")

def colorSort():
    global myVariable, ai_vision_1_objects, screen_precision, console_precision
    while True:
        checkBlue()
        checkRed()
        wait(0.1, SECONDS)
        wait(5, MSEC)

Thread(colorSort)
