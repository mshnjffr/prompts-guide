import json
import requests
from config import Config

# Initialize configuration
config = Config()
# Validate that all required configuration values are present
config.validate()

# --------------------------------------------------------------
# Chain-of-Thought Prompting Example
# --------------------------------------------------------------

# Define the headers and payload
headers = {
    'Authorization': config.sg_token,
    'X-Requested-With': config.x_requested_with,
    'Content-Type': 'application/json'
}

# Chain-of-Thought prompting for complex reasoning
payload = {
    'model': config.model,
    'temperature': 0.1,
    'max_tokens': 4000,
    'messages': [
        {
            'role': 'assistant',
            'content': 'You are an expert problem solver with advanced capabilities in logical reasoning, mathematics, and sequential thinking. When presented with complex problems, break down your reasoning into clear, logical steps. Explain your thought process thoroughly, considering all relevant factors and potential approaches before arriving at a conclusion.'
        },
        {
            'role': 'user',
            'content': """I need help solving this complex logical reasoning problem. Please walk through your thinking step by step.

In a small town, there are three types of people: Truth-tellers who always tell the truth, Liars who always lie, and Alternators who alternate between telling the truth and lying (starting with the truth on their first statement, then lying on their second, and so on).

You meet three people: Alice, Bob, and Charlie.

Alice says: "Bob is a Liar."
Alice then says: "Charlie is not a Truth-teller."
Bob says: "Alice is an Alternator."
Charlie says: "Alice is not a Liar."

What type is each person (Truth-teller, Liar, or Alternator)? Analyze all possibilities systematically until you can determine the unique solution."""
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
        print("CHAIN-OF-THOUGHT REASONING FOR LOGICAL PUZZLE:\n")
        print(content)
        print("\n" + "="*80)
    else:
        print("No message content found in the response")
else:
    print(f"Error: {response.status_code}")
    print(response.text)