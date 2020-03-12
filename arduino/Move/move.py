import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def read():
	line = ser.readline().decode('utf-8').rstrip()
	print(line)

if (__name__=='__main__'):
	
	ser.flush()
	ser.write(b"hi\n")
	sleep(2)
	read()

	ser.write(b"move_front\n")
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
