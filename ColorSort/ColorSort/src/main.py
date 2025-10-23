# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       robobears                                                    #
# 	Created:      10/23/2025, 4:59:43 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def colorSort():
    while True:
        ai_objects = colorSortVision.take_snapshot(AiVision.ALL_AIOBJS)
        if ai_objects and len(ai_objects) > 0:
            if ai_objects[0].id == GameElementsPushBack.RED_BLOCK:
                brain.screen.print("Red Object Detected")
            elif ai_objects[0].id == GameElementsPushBack.BLUE_BLOCK:
                brain.screen.print("Blue Object Detected")
        else:
            brain.screen.print("No Object Detected")
    wait(20, MSEC)

thread_colorSort = Thread(colorSort)

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    while True:
        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()