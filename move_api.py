import flask
from flask import request, jsonify
#from move import move_front, open_hatch, close_hatch

app = flask.Flask(__name__)
app.config["DEBUG"] = True

##########  motor ids #######
fwd1 = 1
fwd2 = 2
bck1 = 3
bck2 = 4
htch = 5
#############################
@app.route('/', methods=['GET'])
def home():
	return '<h1> please use the move_fwd and move_bck methods</h1>'

@app.route('/move_fwd', methods=['POST'])
def move_fwd():
	
	if 'time' in request.args:
		time = int(request.args['time'])
		#mv(fwd1,fwd2,bck1,bck2,time/1000.0)
	else:
		return "Error: No time field provided. Please specify an time"

@app.route('/move_bck', methods=['POST'])
def move_bck():
	
	if 'time' in request.args:
		time = int(request.args['time'])
		#mv(bck1,bck2,fwd1,fwd2,time/1000.0)
	else:
		return "Error: No time field provided. Please specify an time"

@app.route('/open_hatch', methods=['POST'])
def open_hatch():
	#open_hatch(htch)

@app.route('/close_hatch', methods=['POST'])
def close_hatch():
	#close_hatch(htch)

app.run()
