#!/usr/bin/env python3
"""
Scripts to drive a donkey 2 car and train a model for it.
Usage:
    joystick.py (drive) [--model=<model>]
    joystick.py (reset)
"""
import os
import numpy

from docopt import docopt
from PIL import Image
from time import sleep, time
import mss
import pyvjoy
from controller import Joystick

# import parts
# from donkeycar.parts.keras import KerasCategorical

j = pyvjoy.VJoyDevice(1)

def toRange(oldValue, oldMin, oldMax, newMin, newMax):
    return (((oldValue - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin

def setThrottle(value):
    j.set_axis(pyvjoy.HID_USAGE_RZ, value)


def setSteering(value):
    j.set_axis(pyvjoy.HID_USAGE_X, value)


def captureScreen(sct):
    img = sct.grab(sct.monitors[1])
    img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
    return img.resize((160, 120))


def drive():
    while True:
        #setThrottle(0x8000)
        setSteering(0x4000)
        sleep(1)
        #setThrottle(0x0001)
        setSteering(0x0001)
        sleep(1)


if __name__ == '__main__':
    try:
        print("Starting driving")
        drive()
    except Exception as e:
        setThrottle(0)
        setSteering(0)
        raise (e)