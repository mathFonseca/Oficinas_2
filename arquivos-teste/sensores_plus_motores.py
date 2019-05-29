# CamJam EduKit 3 - Robotics
# Worksheet 8 - Line Following Robot

import time  # Import the Time library
from gpiozero import Robot, LineSensor  # Import the GPIO Zero Library

# Set variables for the line detector GPIO pin
pinLineFollowerRight = 11
pinLineFollowerLeft = 8

linesensorright = LineSensor(pinLineFollowerRight)
linesensorleft = LineSensor(pinLineFollowerLeft)
robot = Robot(left=(17,18), right=(22,23))

# Set the relative speeds of the two motors, between 0.0 and 1.0
leftmotorspeed = 0.36
rightmotorspeed = 0.33

motorforward = (leftmotorspeed, rightmotorspeed)
motorbackward = (-leftmotorspeed, -rightmotorspeed)
motorleft = (leftmotorspeed, 0)
motorright = (0, rightmotorspeed)

rightisoverblack = False  # A flag to say the robot can see a black line
leftisoverblack = False  # A flag to say the robot can see a black line
linelost = False  # A flag that is set if the line has been lost


# Define the functions that will be called when the line is
# detected or not detected
def linenotseenright():
    global rightisoverblack, linelost
    print("The right white has been found.")
    rightisoverblack = False
    linelost = False
    robot.value = motorforward


def lineseenright():
    global rightisoverblack
    print("The right white has been lost.")
    rightisoverblack = True

# Define the functions that will be called when the line is
# detected or not detected
def linenotseenleft():
    global leftisoverblack, linelost
    print("The left white has been found.")
    leftisoverblack = False
    linelost = False
    robot.value = motorforward


def lineseenleft():
    global leftisoverblack
    print("The left white has been lost.")
    leftisoverblack = True


# Search for the white
def seeklineright():
    global linelost
    robot.stop()

    print("Seeking white right")

    seektime = 0.15  # Turn for 0.25s
    seekcount = 1  # A count of times the robot has looked for the line
    maxseekcount = 10  # The maximum time to seek the line in one direction

    # Turn the robot left and right until it finds the line
    # Or we have looked long enough
    while seekcount <= maxseekcount:

        # Start the motors turning in a direction
        robot.value = motorright

        # Save the time it is now
        starttime = time.time()

        # While the robot is turning for seektime seconds,
        # check to see whether the line detector is over black
        while (time.time() - starttime) <= seektime:
            if not rightisoverblack:
                robot.value = motorforward
                # Exit the seekline() function returning
                # True - the line was found
                return True

        # The robot has not found the black line yet, so stop
        robot.stop()

        # Increase the seek count
        seekcount += 1

    # The line wasn't found, so return False
    robot.stop()
    print("The right line has been lost - relocate your robot")
    linelost = True
    return False

# Search for the white
def seeklineleft():
    global linelost
    robot.stop()

    print("Seeking white left")

    seektime = 0.15  # Turn for 0.25s
    seekcount = 1  # A count of times the robot has looked for the line
    maxseekcount = 10  # The maximum time to seek the line in one direction

    # Turn the robot left and right until it finds the line
    # Or we have looked long enough
    while seekcount <= maxseekcount:

        # Start the motors turning in a direction
        robot.value = motorleft

        # Save the time it is now
        starttime = time.time()

        # While the robot is turning for seektime seconds,
        # check to see whether the line detector is over black
        while (time.time() - starttime) <= seektime:
            if not leftisoverblack:
                robot.value = motorforward
                # Exit the seekline() function returning
                # True - the line was found
                return True

        # The robot has not found the black line yet, so stop
        robot.stop()

        # Increase the seek count
        seekcount += 1

    # The line wasn't found, so return False
    robot.stop()
    print("The left line has been lost - relocate your robot")
    linelost = True
    return False


# Tell the program what to do with a line is seen
linesensorright.when_line = lineseenright
# And when no line is seen
linesensorright.when_no_line = linenotseenright


# Tell the program what to do with a line is seen
linesensorleft.when_line = lineseenleft
# And when no line is seen
linesensorleft.when_no_line = linenotseenleft

try:
    # repeat the next indented block forever
    robot.value = motorforward
    while True:
        if rightisoverblack and not linelost:
            seeklineright()
        if leftisoverblack and not linelost:
            seeklineleft()


# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    exit()