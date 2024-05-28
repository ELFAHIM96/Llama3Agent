
import os
from langchain_community.llms import Ollama
from typing import Union
from typing import Dict, List
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
import json


os.environ["SERPER_API_KEY"] = "f6f24bddfe9ef74496a3d14f187677136d891dbf"
model  = Ollama(model="llama3")

email = "nigerian prince sending some gold"
is_verbose = False

search_tool = SerperDevTool()
# Create  first agent

classifier = Agent(
    role  = "email classifier",
    goal  = "accurately classify emails based on thier imortance. give  every email one of this ratings: important, casual, or spam",
    backstory="You are an AI assistant whose only job is to classify emails accurately and honestly. Do not be afraid to give emails bad rating if they are not important. your job is to help the user manage thier inbox",
    verbose= is_verbose,
    allow_delegation= False,
    llm= model

)

# Create second agent*

responder = Agent(
    role  = "email responder",
    goal  = "respond to emails in a way that is appropriate to the email's importance first, then casual emails, and ignore spam emails. and based on theimportance of mail write a concise and simple response, uf the email is rated 'important' write a formal responce , if the email is rated casual write a casual responce , and if the email is rated 'spam' ignore the email. no matter what, be very concise",
    backstory="You are an AI assistant whose only job is to respond to emails accurately and honestlt . do not be afraid to ignore emails if they are not important. your job is to help the user manage thier inbox",
    verbose= is_verbose,
    allow_delegation= False,
    llm= model
    )

classify_email = Task(
    description= f"Classify the email {email}", 
    agent= classifier,
    expected_output= "One of these three options: 'important', 'casual', or 'spam'",
    tools= [search_tool]

)

respond_to_email = Task(
    description= f"Respond to the email {email}",
    agent= responder,
    expected_output= "a very concise response  to the email based on the importance provided by the 'classifier' agent."
)

crew = Crew(
    agents= [classifier, responder],
    tasks = [classify_email, respond_to_email],
    verbose= 2,
    process= Process.sequential
)
task1_output = classify_email.output.raw_output
# task2_output = respond_to_email.output.raw_output

def parse_output(output: str) -> Dict[str, str]:
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        # If the output is not a valid JSON, assume some default structure
        return {"classification": "unknown", "response": output.strip()}
output = crew.kickoff()

print(task1_output)
print(task2_output)
print(parse_output(output))


