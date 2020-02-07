from flask import Flask, request
from io import BytesIO
import numpy as np
import pickle
import sys

if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], 'classifier_pickle', 'number_of_bins')
    sys.exit(1)

##datastructure to help support classification of images based on the number of
##bins that are in the system
common_map = {
'recyclable': 'recyclable',
'non-recyclable': 'non-recyclable',
'glass': 'recyclable',
'plastic': 'recyclable',
'paper': 'recyclable',
'trash': 'non-recyclable',
}
MAP = {
2:{
    'metal': 'recyclable',
    'cardboard': 'recyclable',
    **common_map
},
3:{
    'metal': 'metal',
    'cardboard': 'recyclable',
    **common_map
},
4:{
    'metal': 'metal',
    'cardboard': 'cardboard',
    **common_map
}
}[sys.argv[2]]




app = Flask(__name__)
cfer = pickle.load(open(sys.argv[1], 'rb'))
print('loaded', cfer)

@app.route('/classify', methods=['POST'])
def classify():
    return MAP[ cfer.classify( dict(np.load(BytesIO(request.data))) ) ]

@app.route('/update/<label>', methods=['GET'])
def update(label):
    return cfer.update(label)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
