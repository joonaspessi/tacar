import os
import glob
import re
from mss import mss
import mss.tools
from datetime import datetime

from PIL import Image

from controller import Joystick

class Recorder:
    def __init__(self):
        self.joystick = Joystick()
        self.id = 0
        self.dir = ""
        self.isRecording = False
        self.sct = mss.mss()

    def set_directory(self, dirName):
        self.dir = dirName
        file_list = glob.glob('%s/*_*.*' % dirName)
        largest_id = 0
        for fname in file_list:
            res = re.findall("_(\d+).", fname)
            if not res: continue
            if int(res[0]) > largest_id:
                largest_id = int(res[0])
        self.id = largest_id
        return largest_id

    def init_rec(self):
        self.create_metadata()

    def store_rec(self):
        self.capture_joystick(self.joystick, self.id)
        self.capture_screen(self.sct, self.id)
        self.id = self.id + 1
        return self.id

    def start(self):
        self.isRecording = True
        self.create_metadata()
        try:
            with mss.mss() as sct:
                while self.isRecording: 
                    self.capture_joystick(self.joystick, self.id)
                    self.capture_screen(sct, self.id)
                    self.id = self.id + 1
        except Exception as e:
            raise e

    def stop(self):
        self.isRecording = False

    def create_metadata(self):
        if os.path.isfile('%s/meta.json' % self.dir):
            with open('%s/meta.json' % self.dir, 'w') as f:
                f.write('{"inputs":["cam/image_array","user/angle","user/throttle","user/mode"],"types":["image_array","float","float","str"]}')

    def get_image_name(self, id):

        return 'shot_%i.png' % id

    def capture_screen(self, sct, id):
        img = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        resized = img.resize((160, 120))
        resized.save('%s/%s' % (self.dir, self.get_image_name(id)))

    def capture_joystick(self, joystick, id):
        image_name = self.get_image_name(id)
        throttle = joystick.getThrottle()
        steering = joystick.getSteering()
        brake = joystick.getBrake()
        with open('%s/record_%d.json' % (self.dir, id), 'w') as f: 
            f.write('{"cam/image_array":"%s","user/throttle":%i,"user/steering":%i, "user/brake":%i, "user/mode":"user"}' % (image_name, throttle, steering, brake))

    def is_recording(self):
        return self.isRecording

if __name__ == "__main__":
    joystick = Joystick()
    limit = 10000
    print('Limiting recording to', limit)

    print ('\a')
    if os.path.isfile('log/meta.json'):
        with open('log/meta.json', 'w') as f: 
            f.write('{"inputs":["cam/image_array","user/angle","user/throttle","user/mode"],"types":["image_array","float","float","str"]}')
    
    try:
        with mss.mss() as sct:
            counter = 0
            prevSec = datetime.now().time().second
            while True: 
                captureJoystick(joystick, counter)
                captureScreen(sct, counter)
                id = id + 1
                counter = counter + 1
    except Exception as e:
        raise e