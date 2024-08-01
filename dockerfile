# Use an official Python runtime as a parent image
FROM python:3.12-bookworm

# Set the working directory in the container
WORKDIR /usr/src/app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV AZURE_OPENAI_API_BASE=
ENV AZURE_OPENAI_DEPLOYMENT=
ENV AZURE_OPENAI_API_KEY=
ENV OPENAI_API_VERSION=

# Run app.py when the container launches
CMD ["flask", "run"]