from motors import Motors
from time import time, sleep

em = Motors()
magnet1 = 4
magnet2 = 5
def runMagnet():
	em.move_motor(magnet2, 100)
def stopMagnet():
	em.stop_motors()


