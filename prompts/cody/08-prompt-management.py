import json
import requests
import os
from jinja2 import Environment, FileSystemLoader
from config import Config

# Initialize configuration
config = Config()
# Validate that all required configuration values are present
config.validate()

# --------------------------------------------------------------
# Prompt management with Jinja2 templates stored in external files
# --------------------------------------------------------------

# Define the headers for API requests
headers = {
    'Authorization': config.sg_token,
    'X-Requested-With': config.x_requested_with,
    'Content-Type': 'application/json'
}

# Set up Jinja2 environment to load templates from files
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
environment = Environment(loader=FileSystemLoader(template_dir))
template = environment.get_template('prompts.j2')

# Function to get AI response using a rendered template
def get_ai_response(template_name, template_vars):
    # Get the macro from the template based on the type
    if template_name == 'concept':
        rendered_prompt = template.module.concept(template_vars['topic'], template_vars.get('conciseness', False))
    elif template_name == 'language':
        rendered_prompt = template.module.language(template_vars['topic'], template_vars.get('conciseness', False))
    elif template_name == 'pattern':
        rendered_prompt = template.module.pattern(template_vars['topic'], template_vars.get('conciseness', False))
    else:
        raise ValueError(f"Unknown template type: {template_name}")
    
    # Create the payload with the rendered prompt
    payload = {
        'model': config.model,
        'temperature': 0.1,
        'max_tokens': 1000,
        'messages': [
            {
                'role': 'user',
                'content': rendered_prompt
            }
        ]
    }
    
    # Send the request to the completions endpoint
    response = requests.post(
        config.completions,
        headers=headers,
        json=payload
    )
    
    # Extract and return the response
    if response.status_code == 200:
        response_data = response.json()
        if 'choices' in response_data and len(response_data['choices']) > 0:
            message = response_data['choices'][0].get('message', {})
            content = message.get('content', '')
            return content
        else:
            return "No message content found in the response"
    else:
        return f"Error: {response.status_code}\n{response.text}"

# Example 1: Ask about a programming concept
concept_vars = {
    'topic': 'SOLID',
    'conciseness': True
}

# Example 2: Ask about a programming language
language_vars = {
    'topic': 'Python',
    'conciseness': False
}

# Example 3: Ask about a design pattern
pattern_vars = {
    'topic': 'Observer',
    'conciseness': True
}

# Get user input for which template to use
print("\nSelect a prompt template to use:")
print("1. Software Engineering Concept (SOLID)")
print("2. Programming Language (Python)")
print("3. Design Pattern (Observer)")

choice = input("Enter your choice (1-3): ")

if choice == '1':
    template_name = 'concept'
    template_vars = concept_vars
    topic_description = "SOLID principles (concise)"
elif choice == '2':
    template_name = 'language'
    template_vars = language_vars
    topic_description = "Python programming language (detailed)"
elif choice == '3':
    template_name = 'pattern'
    template_vars = pattern_vars
    topic_description = "Observer design pattern (concise)"
else:
    print("Invalid choice, using default (SOLID principles)")
    template_name = 'concept'
    template_vars = concept_vars
    topic_description = "SOLID principles (concise)"

# Get the response
content = get_ai_response(template_name, template_vars)

# Print the response in a formatted way
print("\n" + "="*80 + "\n")
print(f"RESPONSE ABOUT: {topic_description}\n")
print(content)
print("\n" + "="*80)

# Show the actual prompt that was sent (for educational purposes)
print("\nThe template-rendered prompt that was sent:")
print("-"*50)

# Get the rendered template based on the type
if template_name == 'concept':
    rendered_prompt = template.module.concept(template_vars['topic'], template_vars.get('conciseness', False))
elif template_name == 'language':
    rendered_prompt = template.module.language(template_vars['topic'], template_vars.get('conciseness', False))
elif template_name == 'pattern':
    rendered_prompt = template.module.pattern(template_vars['topic'], template_vars.get('conciseness', False))

print(rendered_prompt)
print("-"*50)