from gpiozero import Servo
from time import sleep
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12,50)
p.start(7.5)

myGPIO=18
 
myCorrection=0.50
maxPW=(2.0+myCorrection)/1000
print(maxPW)
minPW=(1.0-myCorrection)/1000
print(minPW)
 
#servo = Servo(myGPIO,min_pulse_width=0.0005,max_pulse_width=0.0025)


while True:
	p.ChangeDutyCycle(7.5)
	sleep(2)
	p.ChangeDutyCycle(12.5)
	sleep(2)
	p.ChangeDutyCycle(2.5)
	sleep(2)
    
