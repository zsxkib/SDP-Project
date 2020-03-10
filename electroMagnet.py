from motors import Motors
from time import time, sleep

em = Motors()
magnet1 = 4
magnet2 = 5
def runMagnet():
<<<<<<< Updated upstream
#	em.move_motor(magnet1, 100)
=======
	#em.move_motor(magnet1, 100)
>>>>>>> Stashed changes
	em.move_motor(magnet2, 100)
def stopMagnet():
	em.stop_motors()


