import ctypes
import time
from sdl2 import SDL_JOYDEVICEADDED, SDL_JOYAXISMOTION, SDL_JoystickOpen, SDL_Init, SDL_INIT_JOYSTICK, SDL_Event, SDL_PollEvent, SDL_JOYBUTTONDOWN, SDL_JOYBUTTONUP

THROTTLE_AXIS = 5
BRAKE_AXIS = 2
STEER_AXIS = 0

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

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
        return self.normalize(self.getAxis(STEER_AXIS), -1, 1)

    def getThrottle(self):
        return self.normalize(self.getAxis(THROTTLE_AXIS),0, 1)

    def getBrake(self):
        return self.getAxis(BRAKE_AXIS)

    def normalize(self, value, min, max):
        return translate(value, -32768, 32767, min, max)
        
if __name__ == "__main__":
    joystick = Joystick()
    while True:
        joystick.update()
        time.sleep(0.5)
        print(joystick.getSteering(), joystick.getThrottle())