from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/getUserInput', methods=['POST', 'GET'])
def page_input():
    return render_template('touchscreen_select_category.html')

@app.route('/idle', methods=['GET'])
def page_idle():
    return render_template('touchscreen_idle.html')

@app.route('/processing', methods=['GET'])
def page_processing():
    return render_template('touchscreen_processing.html')



if __name__ == "__main__":
    app.run(debug=True)
