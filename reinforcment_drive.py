#!/usr/bin/env python3

import controller
from time import sleep

def drive():
    while True:
        controller.joyGet()
        sleep(1)

if __name__ == '__main__':
    try:
        print("Starting controller check sequence")
        drive()
    except Exception as e:
        raise (e)