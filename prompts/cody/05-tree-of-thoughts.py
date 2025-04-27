import json
import requests
from config import Config

# Initialize configuration
config = Config()
# Validate that all required configuration values are present
config.validate()

# --------------------------------------------------------------
# Tree of Thoughts Prompting Example
# --------------------------------------------------------------

# Define the headers and payload
headers = {
    'Authorization': config.sg_token,
    'X-Requested-With': config.x_requested_with,
    'Content-Type': 'application/json'
}

# Tree of Thoughts prompting explores multiple reasoning paths
payload = {
    'model': config.model,
    'temperature': 0.7,  # Higher temperature for more diverse thinking paths
    'max_tokens': 4000,
    'messages': [
        {
            'role': 'assistant',
            'content': 'You are a problem-solving assistant that explores multiple reasoning paths before arriving at a conclusion. For the given problem, generate 3 different approaches, evaluate the pros and cons of each, and then select the best one.'
        },
        {
            'role': 'user',
            'content': 'What would be the best way to reduce traffic congestion in a growing city?'
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
        print("TREE OF THOUGHTS REASONING:\n")
        print(content)
        print("\n" + "="*80)
    else:
        print("No message content found in the response")
else:
    print(f"Error: {response.status_code}")
    print(response.text)