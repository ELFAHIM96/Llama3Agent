# email_processor.py

from langchain_community.llms import Ollama
import json
from typing import Union
from crewai import Agent, Task, Crew, Process

model  = Ollama(model="llama3")

is_verbose = False

# Define your email classifier agent
classifier = Agent(
    role="email classifier",
    goal="accurately classify emails based on their importance. give every email one of these ratings: important, casual, or spam",
    backstory="You are an AI assistant whose only job is to classify emails accurately and honestly. Do not be afraid to give emails a bad rating if they are not important. your job is to help the user manage their inbox",
    verbose=False,
    allow_delegation=False,
    llm=model
)

# Define your email responder agent
responder = Agent(
    role="email responder",
    goal="respond to emails in a way that is appropriate to the email's importance first, then casual emails, and ignore spam emails. and based on the importance of mail write a concise and simple response. If the email is rated 'important' write a formal response, if the email is rated casual write a casual response, and if the email is rated 'spam' ignore the email. no matter what, be very concise",
    backstory="You are an AI assistant whose only job is to respond to emails accurately and honestly. do not be afraid to ignore emails if they are not important. your job is to help the user manage their inbox",
    verbose=False,
    allow_delegation=False,
    llm=model
)

# Function to classify and respond to emails
def process_emails(emails):
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

        output = crew.kickoff()
                # Ensure the output is a dictionary
        if isinstance(output, str):
            output = json.loads(output)  # Convert string representation of dict to actual dict
        responses.append(output)

    
    return responses

# Function to process emails with human interaction
def process_emails_with_human_interaction(emails):
    from human_interaction import human_interaction

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

        output = crew.kickoff()
        # Ensure the output is a dictionary
        response = human_interaction(email, output)
        responses.append(response)
    
    return responses

if __name__ == "__main__":
    # List of emails to process
    emails = [
        "nigerian prince sending some gold",
        "Meeting rescheduled to 3 PM",
        "Reminder: Project deadline tomorrow",
        "Congratulations, you won a lottery"
    ]

    # Process emails with human interaction
    responses = process_emails_with_human_interaction(emails)
    for response in responses:
        print(response)
