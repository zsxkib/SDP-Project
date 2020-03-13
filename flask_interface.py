import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# @app.route('/', methods=['GET'])
# def home():
#     return "<h1>this is the control for the motors. Pls use the move_front, move_back and hatch methods </h1>"


@app.route('/move_front', methods=['GET'])
def move_front():
    move.move_front()
    return ('moved_front')


@app.route('/', methods=['GET'])
def index():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks)



app.run()
