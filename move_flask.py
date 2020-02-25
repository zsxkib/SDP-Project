import flask
import move

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>this is the control for the motors. Pls use the move_front, move_back and hatch methods </h1>"


@app.route('/move_front', methods=['GET'])
def move_front():
    move.move_front()
    return ('moved_front')
@app.route('/move_back', methods=['GET'])
def move_back():
    move.move_back()
    return ('moved_back')


@app.route('/stop_motors', methods=['GET'])
def atop_motors():
    move.stop_motors()
    return ('motors_stopped')

@app.route('/hatch', methods=['GET'])
def hatch():
    move.hatch()
    return ('hatch operated')

app.run(host='0.0.0.0')

