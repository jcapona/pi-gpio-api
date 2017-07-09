from src.pi import Pi
from time import sleep
import RPi.GPIO as GPIO

p = Pi()
p.setOutput(1)
p.write(1, GPIO.HIGH)
sleep(5)
p.write(1, GPIO.LOW)
p.clean()
