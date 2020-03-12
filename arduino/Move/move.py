import serial
from time import sleep

def read():
	line = ser.readline().decode('utf-8').rstrip()
	print(line)

if (__name__=='__main__'):
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	ser.flush()
	ser.write(b"move_front")
	sleep(2)
	read()
	ser.write(b"stop_motors\n")
	sleep(2)
	read()
	ser.write(b"move_back\n")
	sleep(2)
	read()
	ser.write(b"hatch\n")
	sleep(2)
	read()
	ser.write(b"stop_motors")
	sleep(2)
	read()
