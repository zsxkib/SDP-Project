from flask import Flask, request
from io import BytesIO
import numpy as np
import pickle
import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], 'classifier_pickle')
    sys.exit(1)

app = Flask(__name__)
cfer = pickle.load(open(sys.argv[1], 'rb'))
print('loaded', cfer)

@app.route('/classify', methods=['POST'])
def classify():
    return cfer.classify( dict(np.load(BytesIO(request.data))) )

@app.route('/update/<label>', methods=['GET'])
def update(label):
    return cfer.update(label)

if __name__ == '__main__':
    app.run()
