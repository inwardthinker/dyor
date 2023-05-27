import requests
def manage_calendar(input_text):
    return input_text

def generate_chat_response(input_prompt):
    system_prompt = "You are Donna Paulsen from Suits. Answer like her"
    url = "https://api.openai.com/v1/chat/completions"
    # do change the api key too
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"  # Replace with your ChatGPT API key
    }
    data = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_prompt}
        ],
        "model": "gpt-3.5-turbo" 
    }
    
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    
    if "choices" in response_data:
        choices = response_data["choices"]
        if choices and "message" in choices[0] and "content" in choices[0]["message"]:
            return choices[0]["message"]["content"]
    
    return None
