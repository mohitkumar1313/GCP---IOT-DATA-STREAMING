# Use an official Python runtime as a parent image
FROM python:3.13.0-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
# Copy the application code
COPY ./producer /app

# Copy the requirements file explicitly
COPY ./producer/requirements.txt /app/requirements.txt
# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip
# Install any dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose any ports the app might need (e.g., for logging or web access, if needed)
# EXPOSE 80  # Uncomment if you plan to expose a port for web access or debugging

# Define entrypoint to run your producer and consumer scripts
# You can use an entrypoint script that runs both, or run one at a time depending on your use case.

# If you want to run the producer and consumer in the same container, you can use a script to handle that.
CMD ["python", "producer.py"]
