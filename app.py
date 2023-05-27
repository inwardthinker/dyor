from flask import Flask, jsonify, request
from functions import generate_chat_response
from slackinterface import send_message, send_personal_message
app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

@app.route('/run', methods=['POST'])
def run():
    request_data = request.get_json()
    input_text = request_data['input_text']
    response = generate_chat_response(input_text)
    if response:
        output_text = response
    else:
        output_text = "Sorry I didn't get that. I guess I'm too awesome to understand you ;)"
    data = {
        "output_text" : output_text,
    }
    # Replace my user ID with dynamically retrieved user ID
    send_personal_message("U046FAGTWGG", output_text)
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