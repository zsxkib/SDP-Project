from matplotlib import pyplot as plt
from web_client import WebClient
from camera import Camera
from flask import Flask
import subprocess

# after the model is trained, this controller will send requests to the server
# and then move HW

class Controller():
    def __init__(self, url, port):
        self.client = WebClient(url)
        self.port = port
        self.app = Flask(__name__)
        self.recycalbe = ['paper', 'plastic', 'glass']

        # when installing make sure the usb port ids match
        self.camera_top = Camera('1.1.3')
        self.camera_side = Camera('1.2')

    @app.route('/', methods=['GET'])
    def run(self):
        template = open('demo1.html').read()
        image_top = camera_top.capture()
        image_side = camera_side.capture()
        plt.imsave('top.png', image_top)
        plt.imsave('side.png', image_side)
        pred_label = self.client.classify(image_top=image_top, image_side=image_side)
        return template.replace('{pred_label}', pred_label)


    @app.route('/file/<filename>', methods=['GET'])
    def file(self, filename):
        return open(filename, 'rb').read()


    def start(self):
        while(True):
            print("Please select a mode:")
            print("\tInput \"a\" to run")
            print("\tInput else to exit")
            print("> ")
            user_input = str(input()).strip()

            if user_input == 'a':
                result_class = app.run(port=self.port)
                print("The result class is: {}" % (result_class))
                if result_class in self.recycalbe:
                    # move machine to bin 1
                    print("The trash is recycable, dumping to bin 1")
                    pass
                    cmd = "move_forward.py"
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                    output, error = process.communicate()
                else:
                    # move machine to bin 2
                    print("The trash is non-recycable, dumping to bin 2")
                    pass
                    cmd = "move_backward.py"
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                    output, error = process.communicate()
            else:
                print("Thank you. bye!")
                break


if __name__ == '__main__':
    C = Controller(url='http://localhost:5000', port=8088)
    C.start()
