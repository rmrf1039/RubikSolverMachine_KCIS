#!/usr/bin/env python3

import sys
import time
import RPi.GPIO as GPIO

class A4988Nema(object):
    def __init__(self, direction_pin, step_pin, en_pin):
        self.direction_pin = direction_pin
        self.step_pin = step_pin
        self.en_pin = en_pin
        self.onceMoved = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(self.en_pin, GPIO.OUT, initial=True)

    def rotate(self, clockwise=False, steps=200, stepdelay=.005, verbose=False, doInit=True):
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        
        try:
            if not self.onceMoved:
                GPIO.output(self.en_pin, False)
                self.onceMoved = True
                time.sleep(0.0019)
                
            GPIO.output(self.direction_pin, clockwise)
            
            for i in range(steps):
                GPIO.output(self.step_pin, True)
                time.sleep(stepdelay)
                GPIO.output(self.step_pin, False)
                time.sleep(stepdelay)

        except KeyboardInterrupt:
            print("User Keyboard Interrupt : Libmotor:")
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("Libmotor  : Unexpected error:")
        else:
            if verbose:
                print("Clockwise = {}".format(clockwise))
                print("Number of steps = {}".format(steps))
        finally:
            GPIO.output([self.step_pin, self.direction_pin], (False, False))
            
            if doInit:
                time.sleep(.1)
                self.initlize()
            
    def initlize(self):
        self.onceMoved = False
        GPIO.output(self.en_pin, True)