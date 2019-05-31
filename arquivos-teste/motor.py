import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
PWMFrenteEsquerda = GPIO.PWM(11, 20)
PWMTrasEsquerda = GPIO.PWM(13, 20)
PWMFrenteDireita = GPIO.PWM(15, 20)
PWMTrasDireita = GPIO.PWM(16, 20)
PWMFrenteEsquerda.start(0)
PWMTrasEsquerda.start(0)
PWMFrenteDireita.start(0)
PWMTrasDireita.start(0)

def forward(tf):
	PWMFrenteEsquerda.ChangeDutyCycle(30)
	PWMTrasEsquerda.ChangeDutyCycle(0)
	PWMFrenteDireita.ChangeDutyCycle(30)
	PWMTrasDireita.ChangeDutyCycle(0)
	time.sleep(tf)

def stop():
	PWMFrenteEsquerda.ChangeDutyCycle(0)
	PWMTrasEsquerda.ChangeDutyCycle(0)
	PWMFrenteDireita.ChangeDutyCycle(0)
	PWMTrasDireita.ChangeDutyCycle(0)

forward(4)
stop()
