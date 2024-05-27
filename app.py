from langchain_community.llms import ollama

from crewai import Agent, Task, Crew, Process

model  = ollama(model="llama3")

email = "nigerian prince sending some gold"

# Create  first agent

classifier = Agent(
    role  = "email classifier",
    goal  = "accurately classify emails based on thier imortance. give  every email one of this ratings: important, casual, or spam",
    backstory="You are an AI assistant whose only job is to classify emails accurately and honestly. Do not be afraid to give emails bad rating if they are not important. your job is to help the user manage thier inbox",
    verbose= True,
    allow_delegation= False,
    llm= model

)

# Create second agent*

responder = Agent(
    role  = "email responder",
    goal  = "respond to emails in a way that is appropriate to the email's importance first, then casual emails, and ignore spam emails. and based on theimportance of mail write a concise and simple response, uf the email is rated 'important' write a formal responce , if the email is rated casual write a casual responce , and if the email is rated 'spam' ignore the email. no matter what, be very concise",
    backstory="You are an AI assistant whose only job is to respond to emails accurately and honestlt . do not be afraid to ignore emails if they are not important. your job is to help the user manage thier inbox",
    verbose= True,
    allow_delegation= False,
    llm= model
    )

classify_email = Task(
    description= f"Classify the email {email}", 
    agent= classifier,
    expected_output= "One of these three options: 'important', 'casual', or 'spam'"

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

output = crew.kickoff()
print(output)

