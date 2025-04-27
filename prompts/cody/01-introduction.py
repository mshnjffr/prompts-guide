import json
import requests
from config import Config

# Initialize configuration
config = Config()
# Validate that all required configuration values are present
config.validate()

# --------------------------------------------------------------
# Basic prompt example with the Chat Completions API
# --------------------------------------------------------------

# Define the headers and payload
headers = {
    'Authorization': config.sg_token,
    'X-Requested-With': config.x_requested_with,
    'Content-Type': 'application/json'
}

prompt = 'What is SOLID principles? Only provide high level summary without code examples'
payload = {
    'model': config.model,
    'temperature': 0.1,
    'max_tokens': 1000,
    'messages': [
        {
            'role': 'user',
            'content': prompt
        }
    ]
}

# Send the request to the completions endpoint
response = requests.post(
    config.completions,
    headers=headers,
    json=payload
)

# Extract and print only the message content in a readable format
if response.status_code == 200:
    response_data = response.json()
    if 'choices' in response_data and len(response_data['choices']) > 0:
        message = response_data['choices'][0].get('message', {})
        content = message.get('content', '')
        
        # Format and print the content nicely
        print("\n" + "="*80 + "\n")
        print(f"RESPONSE TO: '{prompt}'\n")
        print(content)
        print("\n" + "="*80)
    else:
        print("No message content found in the response")
else:
    print(f"Error: {response.status_code}")
    print(response.text)