import json
import requests
from typing import Dict, List
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
from human_interaction import human_interaction


# Initialize the model
model = Ollama(model="llama3", api_base_url="http://host.docker.internal:11434")

# Define your email classifier agent
classifier = Agent(
    role="email classifier",
    goal="accurately classify emails based on their importance. Give every email one of these ratings: important, casual, or spam",
    backstory="You are an AI assistant whose only job is to classify emails accurately and honestly. Do not be afraid to give emails a bad rating if they are not important. Your job is to help the user manage their inbox",
    verbose=False,
    allow_delegation=False,
    llm=model
)

# Define your email responder agent
responder = Agent(
    role="email responder",
    goal="respond to emails in a way that is appropriate to the email's importance first, then casual emails, and ignore spam emails. Based on the importance of the email, write a concise and simple response. If the email is rated 'important', write a formal response. If the email is rated casual, write a casual response. If the email is rated 'spam', ignore the email. No matter what, be very concise",
    backstory="You are an AI assistant whose only job is to respond to emails accurately and honestly. Do not be afraid to ignore emails if they are not important. Your job is to help the user manage their inbox",
    verbose=False,
    allow_delegation=False,
    llm=model
)

# Function to clean the output
def clean_output(output: str) -> str:
    # Remove unwanted characters like '**\n' and leading/trailing whitespaces
    return output.replace('**\n', '').replace('** \n', '').strip()

# Function to classify and respond to multiple emails
def process_emails(emails: List[str], enable_human_interaction: bool = False) -> List[Dict[str, str]]:
    responses = []
    for email in emails:
        classify_email = Task(
            description=f"Classify the email: {email}",
            agent=classifier,
            expected_output="One of these three options: 'important', 'casual', or 'spam'"
        )

        respond_to_email = Task(
            description=f"Respond to the email: {email}",
            agent=responder,
            expected_output="A very concise response to the email based on the importance provided by the 'classifier' agent."
        )

        crew = Crew(
            agents=[classifier, responder],
            tasks=[classify_email, respond_to_email],
            verbose=2,
            process=Process.sequential
        )

        crew.kickoff()
        
        # Collect and clean outputs
        classify_output = clean_output(classify_email.output.raw_output)
        respond_output = clean_output(respond_to_email.output.raw_output)
        
        if enable_human_interaction:
            output = {'classification': classify_output, 'response': respond_output}
            response = human_interaction(email, output)
            responses.append(response)
        else:
            responses.append({
                'email': email,
                'classification': classify_output,
                'response': respond_output
            })
    
    return responses

if __name__ == "__main__":
    # List of emails to process
    emails = [
        "nigerian prince sending some gold",
        "Meeting rescheduled to 3 PM",
        "Reminder: Project deadline tomorrow",
        "Congratulations, you won a lottery"
    ]

    # Enable or disable human interaction
    enable_human_interaction = True  # Set to False to disable human interaction

    # Process the emails
    results = process_emails(emails, enable_human_interaction)
    for result in results:
        print(result)

