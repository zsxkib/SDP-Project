import serial
import time
if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	ser.flush()
	i=0
	while True:
		ser.write(b("Hello from Raspberry Pi! "+str(i)+"\n"))
		i+=1
		line = ser.readline().decode('utf-8').rstrip()
		print(line)
		time.sleep(1)
