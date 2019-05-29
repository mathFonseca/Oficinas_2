from gpiozero import Robot
import time

robot = Robot(left=(22, 23), right=(17, 21))

#time.sleep(30)

robot.forward(0.5)
time.sleep(1)
robot.right(0.5)
time.sleep(0.5)
robot.left(0.5)
time.sleep(0.5)
