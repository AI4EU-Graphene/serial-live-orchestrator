# Use the official Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy all files from the cube_node folder
COPY . .

# Install Flask
RUN pip install --no-cache-dir flask

# Expose port 5001 (used by cube_service.py)
EXPOSE 5001

# Run the app
CMD ["python", "cube_service.py"]
