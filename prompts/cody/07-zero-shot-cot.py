import json
import requests
from config import Config

# Initialize configuration
config = Config()
# Validate that all required configuration values are present
config.validate()

# --------------------------------------------------------------
# Zero-Shot Chain-of-Thought Prompting Example
# --------------------------------------------------------------

# Define the headers and payload
headers = {
    'Authorization': config.sg_token,
    'X-Requested-With': config.x_requested_with,
    'Content-Type': 'application/json'
}

# Zero-Shot Chain-of-Thought prompting encourages reasoning without examples
payload = {
    'model': config.model,
    'temperature': 0.1,
    'max_tokens': 4000,
    'messages': [
        {
            'role': 'assistant',
            'content': 'You are a helpful assistant that solves problems carefully.'
        },
        {
            'role': 'user',
            'content': 'If John has 5 pears, then eats 2, and buys 5 more, then gives 3 to his friend, how many pears does he have? Let\'s think through this step by step.'
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
        print("ZERO-SHOT CHAIN-OF-THOUGHT REASONING:\n")
        print(content)
        print("\n" + "="*80)
    else:
        print("No message content found in the response")
else:
    print(f"Error: {response.status_code}")
    print(response.text)