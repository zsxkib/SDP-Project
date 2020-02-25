import requests
import time
response = requests.get('http://192.168.192.101:5000/hatch')
response = requests.get('http://192.168.192.101:5000/move_front')
time.sleep(2)
response = requests.get('http://192.168.192.101:5000/move_back')
time.sleep(2)
response = requests.get('http://192.168.192.101:5000/stop_motors')

print(response.status_code)
