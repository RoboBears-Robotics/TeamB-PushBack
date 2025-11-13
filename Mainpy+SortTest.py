#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
left_motor_a = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT13, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain_inertial = Inertial(Ports.PORT5)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 219.44, 320, 40, MM, 1)
FrontLandM = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
TopMotors = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
BackMiddle = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
BackLower = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
# AI Vision Color Descriptions
ai_vision_1__RedBlock = Colordesc(1, 124, 40, 61, 12, 0.25)
ai_vision_1__BlueBlock = Colordesc(2, 35, 90, 135, 18, 0.34)
# AI Vision Code Descriptions
ai_vision_1 = AiVision(Ports.PORT16, ai_vision_1__RedBlock, ai_vision_1__BlueBlock)
BumperFront = DigitalOut(brain.three_wire_port.a)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    drivetrain_inertial.calibrate()
    while drivetrain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


# Calibrate the Drivetrain
calibrate_drivetrain()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            # stop the motors if the brain is calibrating
            if drivetrain_inertial.is_calibrating():
                left_drive_smart.stop()
                right_drive_smart.stop()
                while drivetrain_inertial.is_calibrating():
                    sleep(25, MSEC)
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            drivetrain_left_side_speed = controller_1.axis3.position() + controller_1.axis1.position()
            drivetrain_right_side_speed = controller_1.axis3.position() - controller_1.axis1.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration

# Begin project code
ai_vision_1_objects = []
ai_vision_1_index = 0
screen_precision = 0
console_precision = 0

buttonXActive = False
buttonBActive = False
buttonUpActive = False
buttonLRActive = False
buttonDownActive = False

drivetrain.set_drive_velocity(100, PERCENT)

def buttonBFunct():
    BackMiddle.stop()
    TopMotors.stop()
    FrontLandM.stop()
    BackLower.stop()
    buttonXActive = False
    buttonUpActive = False
    buttonLRActive = False
    buttonDownActive = False
    global buttonBActive
    if not buttonBActive:
        FrontLandM.spin(FORWARD)
        BackLower.spin(REVERSE)
        buttonBActive = True
    else:
        FrontLandM.stop()
        TopMotors.stop()
        BackLower.stop()
        buttonBActive = False

def buttonXFunct():
    BackMiddle.stop()
    TopMotors.stop()
    FrontLandM.stop()
    BackLower.stop()
    buttonBActive = False
    buttonUpActive = False
    buttonLRActive = False
    buttonDownActive = False
    global buttonXActive
    if not buttonXActive:
        FrontLandM.spin(FORWARD)
        BackLower.spin(FORWARD)
        BackMiddle.spin(REVERSE)
        buttonXActive = True
    else:
        FrontLandM.stop()
        BackLower.stop()
        BackMiddle.stop()
        buttonXActive = False

def buttonUpFunct():
    BackMiddle.stop()
    TopMotors.stop()
    FrontLandM.stop()
    BackLower.stop()
    buttonBActive = False
    buttonXActive = False
    buttonLRActive = False
    buttonDownActive = False
    global buttonUpActive
    if not buttonUpActive:
        FrontLandM.spin(FORWARD)
        BackLower.spin(REVERSE)
        TopMotors.spin(FORWARD)
        BackMiddle.spin(FORWARD)
        buttonUpActive = True
    else:
        FrontLandM.stop()
        BackLower.stop()
        TopMotors.stop()
        BackMiddle.stop()
        buttonUpActive = False

def buttonLRFunct():
    BackMiddle.stop()
    TopMotors.stop()
    FrontLandM.stop()
    BackLower.stop()
    buttonBActive = False
    buttonXActive = False
    buttonUpActive = False
    buttonDownActive = False
    global buttonLRActive
    if not buttonLRActive:
        FrontLandM.spin(FORWARD)
        BackLower.spin(REVERSE)
        BackMiddle.spin(FORWARD)
        TopMotors.spin(REVERSE)
        buttonLRActive = True
    else:
        FrontLandM.stop()
        BackLower.stop()
        BackMiddle.stop()
        TopMotors.stop()
        buttonLRActive = False

def buttonDownFunct():
    BackMiddle.stop()
    TopMotors.stop()
    FrontLandM.stop()
    BackLower.stop()
    buttonBActive = False
    buttonXActive = False
    buttonUpActive = False
    buttonLRActive = False
    global buttonDownActive
    if not buttonDownActive:
        FrontLandM.spin(REVERSE)
        BackMiddle.spin(FORWARD)
        BackLower.spin(REVERSE)
        buttonDownActive = True
    else:
        FrontLandM.stop()
        BackMiddle.stop()
        BackLower.stop()
        buttonDownActive = False

def stopall():
    FrontLandM.stop()
    TopMotors.stop()
    BackMiddle.stop()
    BackLower.stop()
    global buttonBActive, buttonXActive, buttonUpActive, buttonLRActive, buttonDownActive
    buttonBActive = False
    buttonXActive = False
    buttonUpActive = False
    buttonLRActive = False
    buttonDownActive = False

bumperFrontValue = False

def bumperFunct():
    global bumperFrontValue
    if bumperFrontValue:
        BumperFront.set(False)
        bumperFrontValue = False
    else:
        BumperFront.set(True)
        bumperFrontValue = True


def upOutputStart():
    upOutputThread = Thread(upOutput)

def upOutput():
    global ai_vision_1_objects, ai_vision_1_index, screen_precision, console_precision
    while controller_1.buttonL1.pressing():
        FrontLandM.spin(FORWARD)
        TopMotors.spin(FORWARD)
        BackMiddle.spin(FORWARD)
        FrontLandM.spin(FORWARD)
        ai_vision_1_objects = ai_vision_1.take_snapshot(ai_vision_1__RedBlock)
        if ai_vision_1_objects[ai_vision_1_index].width >= 270:
            if ai_vision_1_objects[ai_vision_1_index].centerX >= 150 or ai_vision_1_objects[ai_vision_1_index].centerX <= 170:
                brain.screen.clear_row(1)
                brain.screen.set_cursor(brain.screen.row(), 1)
                brain.screen.set_cursor(1, 1)
                brain.screen.print("Detected Red")
                BackLower.spin(FORWARD)
                wait(1, SECONDS)
        else:
            BackLower.spin(REVERSE)
            brain.screen.clear_row(1)
            brain.screen.set_cursor(brain.screen.row(), 1)
        ai_vision_1_objects = ai_vision_1.take_snapshot(ai_vision_1__BlueBlock)
        if ai_vision_1_objects[ai_vision_1_index].width >= 150:
            if ai_vision_1_objects[ai_vision_1_index].centerX >= 100 or ai_vision_1_objects[ai_vision_1_index].centerX <= 200:
                brain.screen.clear_row(2)
                brain.screen.set_cursor(brain.screen.row(), 1)
                brain.screen.set_cursor(2, 1)
                brain.screen.print("Detected Blue")
                BackLower.spin(FORWARD)
        else:
            BackLower.spin(REVERSE)
            brain.screen.clear_row(2)                
            brain.screen.set_cursor(brain.screen.row(), 1)
        wait(5, MSEC)
        FrontLandM.stop()
        TopMotors.stop()
        BackMiddle.stop()
        BackLower.stop()
        FrontLandM.stop()

controller_1.buttonR2.pressed(bumperFunct)
controller_1.buttonL2.pressed(stopall)
controller_1.buttonL1.pressed(upOutputStart)
controller_1.buttonR1.pressed(bumperFunct)
controller_1.buttonX.pressed(buttonXFunct)
controller_1.buttonB.pressed(buttonBFunct)
controller_1.buttonUp.pressed(buttonUpFunct)
controller_1.buttonLeft.pressed(buttonLRFunct)
controller_1.buttonRight.pressed(buttonLRFunct)
controller_1.buttonDown.pressed(buttonDownFunct)

# def checkBlue():
#     global myVariable, ai_vision_1_objects, screen_precision, console_precision
#     brain.screen.set_font(FontType.MONO40)
#     brain.screen.clear_row(1)
#     brain.screen.set_cursor(brain.screen.row(), 1)
#     brain.screen.set_cursor(1, 1)
#     ai_vision_1_objects = ai_vision_21.take_snapshot(ai_vision_21__BlueBlock)
#     if ai_vision_1_objects and len(ai_vision_1_objects) > 0:
#         brain.screen.print("Blue Object Found")
#     else:
#         brain.screen.print("No Blue Object")

# def checkRed():
#     global myVariable, ai_vision_1_objects, screen_precision, console_precision
#     brain.screen.set_font(FontType.MONO40)
#     brain.screen.clear_row(3)
#     brain.screen.set_cursor(brain.screen.row(), 1)
#     brain.screen.set_cursor(3, 1)
#     ai_vision_1_objects = ai_vision_21.take_snapshot(ai_vision_21__RedBlock)
#     if ai_vision_1_objects and len(ai_vision_1_objects) > 0:
#         brain.screen.print("Red Object Found")
#     else:
#         brain.screen.print("No Red Object")

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
    brain.screen.clear_screen()
    # place driver control in this while loop
    while True:
        wait(20, MSEC)

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

# controller_1.buttonA.pressed(FrontLMForward)
# controller_1.buttonB.pressed(FrontLMReverse)
# controller_1.buttonX.pressed(TopMotorForward)
# controller_1.buttonY.pressed(TopMotorReverse)
# controller_1.buttonR1.pressed(BackMiddleForward)
# controller_1.buttonR2.pressed(BackMiddleReverse)
# controller_1.buttonL1.pressed(BackLowerForward)
# controller_1.buttonL2.pressed(BackLowerReverse)

# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()