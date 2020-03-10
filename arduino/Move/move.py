import serial
from time import sleep

if (__name__=='__main__'):
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	ser.flush()
	
	ser.write(b"move_front\n")
	sleep(2)
	ser.write(b"stop_motors\n")
	sleep(2)
	ser.write(b"move_back\n")
	sleep(2)
	ser.write(b"hatch\n")
	sleep(2)
	ser.write(b"stop_motors\n")
	sleep(2)
