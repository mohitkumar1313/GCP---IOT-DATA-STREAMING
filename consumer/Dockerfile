# Use an official Python runtime as a parent image
FROM python:3.13.0-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code
COPY ./consumer /app

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose any necessary ports (optional)
# EXPOSE 80  # Uncomment if exposing a port

# Use an entrypoint script for flexibility
COPY ./consumer/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
