from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from io import BytesIO
import numpy as np
import pickle
import sys

# if len(sys.argv) != 3:
#     print('Usage:', sys.argv[0], 'classifier_pickle', 'number_of_bins')
#     sys.exit(1)


# ##datastructure to help support classification of images based on the number of
# ##bins that are in the system
# common_map = {
# 'recyclable': 'recyclable',
# 'non-recyclable': 'non-recyclable',
# 'glass': 'recyclable',
# 'plastic': 'recyclable',
# 'paper': 'recyclable',
# 'trash': 'non-recyclable',
# }
# MAP = {
# 2:{
#     'metal': 'recyclable',
#     'cardboard': 'recyclable',
#     **common_map
# },
# 3:{
#     'metal': 'metal',
#     'cardboard': 'recyclable',
#     **common_map
# },
# 4:{
#     'metal': 'metal',
#     'cardboard': 'cardboard',
#     **common_map
# }
# }[int(sys.argv[2])]




app = Flask(__name__)
# cfer = pickle.load(open(sys.argv[1], 'rb'))
# print('loaded', cfer)

@app.route('/classify', methods=['POST'])
def classify():
    return 'trash'

@app.route('/update/<label>', methods=['GET'])
def update(label):
    return None


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/getUserInput', methods=['POST', 'GET'])
def page_input():
    if request.method == 'POST':
        print("detected post request")
        print(request.form)
        print(request.form.get('c1'))
    elif request.method == 'GET':
        pass
    return render_template('touchscreen_select_category.html')

@app.route('/idle', methods=['GET'])
def page_idle():
    return render_template('touchscreen_idle.html')

@app.route('/processing', methods=['GET'])
def page_processing():
    return render_template('touchscreen_processing.html')


if __name__ == "__main__":
    app.run(debug=True)
