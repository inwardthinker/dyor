import os
from flask import Flask, jsonify, request
from functions import generate_chat_response, generate_chat_response_openAI
from slackinterface import send_personal_message
from calendar_model import CalendarModel
from dotenv import load_dotenv, find_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
load_dotenv(find_dotenv())

# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize the Flask app
# Flask is a web application framework written in Python
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)
calendar_model = CalendarModel()

@app.event("app_mention")
def handle_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    text = body["event"]["text"]

    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()

    response1 = generate_chat_response_openAI(text)
    say(response1)
    response = generate_chat_response(text, calendar_model)
    if response:
        output_text = response
        say(output_text)

@flask_app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

@flask_app.route('/run', methods=['POST'])
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
    # currently this is @charan
    send_personal_message("U03HDBHPFEV", output_text)
    return jsonify(data)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Route for handling Slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    return handler.handle(request)

if __name__=='__main__':
    flask_app.run(debug=True, port=8001)