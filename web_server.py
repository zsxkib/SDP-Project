from classifier import Classifier
from flask import Flask, request
from io import BytesIO
import numpy as np

app = Flask(__name__)
cfer = Classifier()

@app.route('/classify', methods=['POST'])
def classify():
    return cfer.classify( np.load(BytesIO(request.data)) )

@app.route('/update/<label>', methods=['GET'])
def update(label):
    return cfer.update(label)

if __name__ == '__main__':
    app.run()
