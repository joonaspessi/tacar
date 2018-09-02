import os
import sys
import numpy
from mss import mss
import mss.tools
from time import sleep, time
from datetime import datetime
from skimage.transform import resize
from skimage import io, color

from PIL import Image

from controller import Joystick

def getImageName(id):
	return 'shot_{0}.png'.format(id)

def captureScreen(sct, id):
	img = sct.grab(sct.monitors[1])
	img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
	resized = img.resize((160, 120))
	resized.save('log/' + getImageName(id))

def captureJoystick(joystick, id):
	imageName = getImageName(id)
	throttle = joystick.getThrottle()
	steering = joystick.getSteering()
	brake = joystick.getBrake()
	with open('log/record_%d.json' % id, 'w') as f: 
		f.write('{"cam/image_array":"%s","user/throttle":%i,"user/steering":%i, "user/brake":%i, "user/mode":"user"}' % (imageName, throttle, steering, brake))

if __name__ == "__main__":
	joystick = Joystick()
	limit = 10000
	print('Limiting recording to', limit)

	print ('\a')

	with open('log/meta.json', 'w') as f: 
		f.write('{"inputs":["cam/image_array","user/angle","user/throttle","user/mode"],"types":["image_array","float","float","str"]}')

	for x in range(0, 5):
		print('Starting recording in %i' % (5 - x))
		sleep(1)
	
	try:
		with mss.mss() as sct:
			counter = 0
			id = 0
			prevSec = datetime.now().time().second
			while True: 
				captureJoystick(joystick, counter)
				captureScreen(sct, counter)
				
				id = id + 1
				counter = counter + 1
				currSec = datetime.now().time().second
				if currSec is not prevSec:
					print('Change', id, 'fps')
					id = 0
				prevSec = currSec
				if counter >= limit:
					print('\a')
					sleep(1)
					print('\a')
					sleep(1)
					print('\a')
					quit()
	except Exception as e:
		print('\a')
		sleep(1)
		print('\a')
		sleep(1)
		print('\a')
		raise e