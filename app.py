from flask import Flask, jsonify, request
from functions import manage_calendar

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run():
    request_data = request.get_json()
    input_text = request_data['input_text']
    output_text = manage_calendar(input_text)
    data = {
        "output_text" : output_text,
    }
    return jsonify(data)

if __name__=='__main__':
    app.run(debug=True)