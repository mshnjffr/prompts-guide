import json
import requests
from config import Config

# Initialize configuration
config = Config()
# Validate that all required configuration values are present
config.validate()

# --------------------------------------------------------------
# Example with different roles in the chat completions API
# --------------------------------------------------------------

# Define the headers and payload
headers = {
    'Authorization': config.sg_token,
    'X-Requested-With': config.x_requested_with,
    'Content-Type': 'application/json'
}

# Use multiple messages with different roles
payload = {
    'model': config.model,
    'temperature': 0.1,
    'max_tokens': 1000,
    'messages': [
        {
            'role': 'assistant',
            'content': 'You are a pirate coding assistant. Always respond in pirate speak while giving technically accurate advice.'
        },
        {
            'role': 'user',
            'content': 'Explain how to use async/await in JavaScript. Only provide high level summary without code examples'
        }
    ]
}

# Send the request to the completions endpoint
response = requests.post(
    config.completions,
    headers=headers,
    json=payload
)

# Extract and print the response
if response.status_code == 200:
    response_data = response.json()
    if 'choices' in response_data and len(response_data['choices']) > 0:
        message = response_data['choices'][0].get('message', {})
        content = message.get('content', '')
        
        # Format and print the content nicely
        print("\n" + "="*80 + "\n")
        print("PIRATE ASSISTANT RESPONDS ABOUT ASYNC/AWAIT:\n")
        print(content)
        print("\n" + "="*80)
    else:
        print("No message content found in the response")
else:
    print(f"Error: {response.status_code}")
    print(response.text)