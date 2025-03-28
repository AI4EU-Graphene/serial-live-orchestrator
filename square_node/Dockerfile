# Use the official Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current folder contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir flask

# Expose port 5000
EXPOSE 5000

# Define the command to run the app
CMD ["python", "square_service.py"]
