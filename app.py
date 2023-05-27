from flask import Flask, jsonify, request
from functions import manage_calendar
from slackinterface import send_message
app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

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

# Handle incoming requests from Slack
@app.route("/slack/events", methods=["POST"])
def slack_events():
    payload = request.get_json()
    
    # Check if the event is a message event
    if payload["event"]["type"] == "message":
        channel_id = payload["event"]["channel"]
        message = payload["event"]["text"]
        
        # Pass the message to AI model here and retrieve the response
        # ---------------INSERT HERE-----------------


        # Send the response to the Slack channel
        send_message(channel_id, f"You said: {message}")
        
    return "OK"