# Use Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Flask
RUN pip install --no-cache-dir flask
RUN pip install --no-cache-dir pandas

# Expose the port used by the app
EXPOSE 5002

# Run the service
CMD ["python", "forecast_service.py"]