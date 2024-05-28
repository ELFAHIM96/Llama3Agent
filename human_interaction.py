# human_interaction.py

def human_interaction(email, output):
    # Assuming output is a dictionary with 'classification' and 'response' keys
    classification = output.get('classification', 'Unknown')  # Extract classification from output
    print(f"Email: {email}")
    print(f"Classification: {classification}")
    human_verification = input("Is the classification correct? (yes/no): ")
    if human_verification.lower() != 'yes':
        classification = input("Enter the correct classification (important/casual/spam): ")

    response = output.get('response', 'No response generated')  # Extract response from output
    print(f"Initial Response: {response}")
    response_modification = input("Do you want to modify the response? (yes/no): ")
    if response_modification.lower() == 'yes':
        response = input("Enter the modified response: ")

    return {
        'email': email,
        'classification': classification,
        'response': response
    }
