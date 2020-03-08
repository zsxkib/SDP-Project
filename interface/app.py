from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/123', methods=['GET'])
def page2():
    return render_template('base.html')



if __name__ == "__main__":
    app.run(debug=True)
