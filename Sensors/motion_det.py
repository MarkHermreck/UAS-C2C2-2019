import RPi.GPIO as GPIO
import time

class motion_det(object):
    GPIO.setmode(GPIO.BOARD) 
    pir = 8 #Assign pin 8 to PIR
    led = 10 #Assign pin 10 to LED
    GPIO.setup(pir, GPIO.IN) #Setup GPIO pin PIR as input
    GPIO.setup(led, GPIO.OUT) #Setup GPIO pin for LED as output
    time.sleep(2) #Give sensor time to startup

    def motion_data():
        try:
            if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
                GPIO.output(led, True) #Turn on LED
                time.sleep(4) #Keep LED on for 4 seconds
                GPIO.output(led, False) #Turn off LED
                time.sleep(0.1)
                return True
            else:
                return False
        except KeyboardInterrupt:
            pass