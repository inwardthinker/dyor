# slack.py
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = os.environ.get("SLACK_API_TOKEN")  # Set your bot token as an environment variable
client = WebClient(token=slack_token)

# Send a message to a Slack channel
def send_message(channel_id, message):
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        return "Message sent successfully"
    except SlackApiError as e:
        return f"Error sending message: {e.response['error']}"

# Retrieve messages from a Slack channel
def retrieve_messages(channel_id):
    try:
        response = client.conversations_history(
            channel=channel_id,
            limit=10  # Number of messages to retrieve
        )
        messages = response["messages"]
        return messages
    except SlackApiError as e:
        return f"Error retrieving messages: {e.response['error']}"