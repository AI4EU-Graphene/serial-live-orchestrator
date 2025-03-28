# Use the official lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY preprocessor_service.py .

# Install required libraries
RUN pip install --no-cache-dir pandas flask

# Expose the service port
EXPOSE 5005

# Run the Flask app
CMD ["python", "preprocessor_service.py"]