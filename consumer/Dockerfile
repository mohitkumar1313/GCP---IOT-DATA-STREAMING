# Use an official Python runtime as a parent image
FROM python:3.13.0-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./consumer /app

# Copy the requirements file explicitly
COPY ./consumer/requirements.txt /app/requirements.txt

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Use CMD to define the default command to run the consumer script
CMD ["python", "consumer.py"]
