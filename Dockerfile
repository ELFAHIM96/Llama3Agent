
FROM alpine:3.10

# Install Python and pip
RUN apk update && apk add --no-cache python3 \
    && python3 -m ensurepip \
    && pip3 install --no-cache --upgrade pip setuptools

WORKDIR /bin/src/app

# Copy the requirements file first for better caching
COPY requirements.txt /bin/src/app/

# Install dependencies
RUN pip3 install -r /bin/src/app/requirements.txt

# Copy the rest of the application code
COPY . /bin/src/app/

CMD ["python3", "app.py"]

