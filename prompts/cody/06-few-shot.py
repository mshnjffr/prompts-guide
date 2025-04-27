import json
import requests
from config import Config

# Initialize configuration
config = Config()
# Validate that all required configuration values are present
config.validate()

# --------------------------------------------------------------
# Few-Shot Prompting Example
# --------------------------------------------------------------

# Define the headers and payload
headers = {
    'Authorization': config.sg_token,
    'X-Requested-With': config.x_requested_with,
    'Content-Type': 'application/json'
}

# Few-shot prompting provides examples to guide the model's responses
payload = {
    'model': config.model,
    'temperature': 0.1,
    'max_tokens': 4000,
    'messages': [
        {
            'role': 'assistant',
            'content': 'You are a sentiment analysis assistant.'
        },
        {
            'role': 'user',
            'content': """Analyze the sentiment of the following reviews as positive, negative, or neutral:

Example 1: "The food was amazing and the service was excellent!" 
Sentiment: Positive

Example 2: "I waited for an hour and the food was cold when it arrived."
Sentiment: Negative

Example 3: "The restaurant was clean and the prices were reasonable."
Sentiment: Positive

Now analyze: "The staff was friendly but the food was mediocre at best."""
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
        print("FEW-SHOT PROMPTING RESULT:\n")
        print(content)
        print("\n" + "="*80)
    else:
        print("No message content found in the response")
else:
    print(f"Error: {response.status_code}")
    print(response.text)