import json
import requests
import os
from config import Config
from prompt_manager import PromptManager

# Initialize configuration
config = Config()
# Validate that all required configuration values are present
config.validate()

# --------------------------------------------------------------
# Using the PromptManager with the ticket_analysis template
# --------------------------------------------------------------

# Define the headers for API requests
headers = {
    'Authorization': config.sg_token,
    'X-Requested-With': config.x_requested_with,
    'Content-Type': 'application/json'
}

# Example ticket data - we'll provide options for the user to choose from
example_tickets = {
    'helpdesk': {
        'pipeline': 'helpdesk',  # This determines which conditional section is shown
        'name': 'Support Bot',
        'company': 'TechGear',
        'ticket': '''
Sender: mark.johnson@techgear.internal
Subject: Unable to access shared drive
Body: Hi IT team, I'm having trouble accessing the marketing shared drive since this morning. 
I get a "permission denied" error when I try to open any files. 
This is urgent as I need to update some materials for tomorrow's meeting.
'''
    },
    'customer': {
        'pipeline': 'customer',
        'name': 'Customer Service AI',
        'company': 'TechGear',
        'ticket': '''
Sender: sarah.smith@gmail.com
Subject: Product not working as expected
Body: Hello, I purchased your TechGear Pro 3000 last week and have been experiencing problems with battery life. 
The product description states 8 hours, but I'm only getting about 3 hours of use before needing to recharge. 
Is this normal or is my unit defective? I have the receipt if a return is needed.
'''
    },
    'billing': {
        'pipeline': 'support',
        'name': 'Billing Support',
        'company': 'TechGear',
        'ticket': '''
Sender: robert.jones@outlook.com
Subject: Double charge on my account
Body: I noticed I was charged twice for my TechGear subscription this month (on the 3rd and again on the 10th). 
Please refund the duplicate charge as soon as possible. My account number is TG-4582390.
'''
    }
}

# Function to get AI response using the PromptManager
def get_ai_response(template_name, template_vars):
    # Get the rendered prompt using PromptManager
    try:
        rendered_prompt = PromptManager.get_prompt(template_name, **template_vars)
        
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
    except Exception as e:
        return f"Error rendering template: {str(e)}"

# Get information about the template
template_info = PromptManager.get_template_info('ticket_analysis')

# Display template information
print("\nTicket Analysis Template Information:")
print(f"Description: {template_info['description']}")
print(f"Author: {template_info['author']}")
print(f"Required variables: {', '.join(template_info['variables'])}")
print()

# Get user input for which ticket to analyze
print("Select a ticket type to analyze:")
print("1. Internal Helpdesk Ticket (IT access issue)")
print("2. Customer Support Ticket (Product issue)")
print("3. Billing Support Ticket (Double charge)")

choice = input("Enter your choice (1-3): ")

# Set the template variables based on the user's choice
if choice == '1':
    template_vars = example_tickets['helpdesk']
    ticket_type = "Internal Helpdesk Ticket"
elif choice == '2':
    template_vars = example_tickets['customer']
    ticket_type = "Customer Support Ticket"
elif choice == '3':
    template_vars = example_tickets['billing']
    ticket_type = "Billing Support Ticket"
else:
    print("Invalid choice, using default (Customer Support Ticket)")
    template_vars = example_tickets['customer']
    ticket_type = "Customer Support Ticket"

# Get and display the AI response
content = get_ai_response('ticket_analysis', template_vars)

# Print the response in a formatted way
print("\n" + "="*80 + "\n")
print(f"TICKET ANALYSIS FOR: {ticket_type}\n")
print(content)
print("\n" + "="*80)

# Show the actual prompt that was sent (for educational purposes)
print("\nThe template-rendered prompt that was sent:")
print("-"*80)
print(PromptManager.get_prompt('ticket_analysis', **template_vars))
print("-"*80)