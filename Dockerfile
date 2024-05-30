
# Use the official Python image from the Docker Hub
FROM python:3.10.14-slim

# Use the official Python image with version 3.10.14
FROM python:3.10.14-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the script
CMD ["python", "multi_mail.py"]
