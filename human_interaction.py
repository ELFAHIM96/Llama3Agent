# human_interaction.py
from typing import Dict
def human_interaction(email: str, output: Dict[str, str]) -> Dict[str, str]:
    # Extract classification and response from output
    classification = output.get('classification', 'Unknown')
    response = output.get('response', 'No response generated')
    
    print(f"Email: {email}")
    print(f"Classification: {classification}")
    human_verification = input("Is the classification correct? (yes/no): ")
    
    if human_verification.lower() != 'yes':
        classification = input("Enter the correct classification based on mail  (important/casual/spam): ")
    
    print(f"Initial Response: {response}")
    response_modification = input("Do you want to modify the response :? (yes/no): ")
    
    if response_modification.lower() == 'yes':
        response = input("Enter the modified response: ")
    
    return {
        'classification': classification,
        'response': response
    }

