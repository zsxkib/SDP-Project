from flask import Flask, request, send_from_directory
import json

app = Flask(__name__)
all_jsonl = open('all.jsonl', 'a')

@app.route('/<filename>', methods=['GET'])
def mystatic(filename):
    return send_from_directory('static', filename) #open(f'static/{filename}', 'rb').read()

@app.route('/upload', methods=['POST'])
def upload():
    d = request.get_json(force=True)
    all_jsonl.write(json.dumps(d) + '\n')
    return 'success'

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
