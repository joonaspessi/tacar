import ctypes
import time
from sdl2 import *

THROTTLE_AXIS = 5
BRAKE_AXIS = 2
STEER_AXIS = 0

class Joystick:
    def __init__(self):
        SDL_Init(SDL_INIT_JOYSTICK)
        self.axis = {0:0, 1:0, 2:-32768, 3:0, 4:0, 5:-32768}
        self.button = {0:False, 1:False, 2:False, 3:False, 4:False, 5:False}
    
    def update(self):
        event = SDL_Event()
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_JOYDEVICEADDED:
                self.device = SDL_JoystickOpen(event.jdevice.which)
            elif event.type == SDL_JOYAXISMOTION:
                self.axis[event.jaxis.axis] = event.jaxis.value
            elif event.type == SDL_JOYBUTTONDOWN:
                self.button[event.jbutton.button] = True
            elif event.type == SDL_JOYBUTTONUP:
                self.button[event.jbutton.button] = False

    def getAxis(self, axis):
        self.update()
        return self.axis[axis]

    def getSteering(self):
        return self.getAxis(STEER_AXIS)

    def getThrottle(self):
        return self.getAxis(THROTTLE_AXIS)

    def getBrake(self):
        return self.getAxis(BRAKE_AXIS)
        
if __name__ == "__main__":
    joystick = Joystick()
    while True:
        joystick.update()
        time.sleep(0.5)
        print(joystick.axis)