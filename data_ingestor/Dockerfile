FROM python:3.12-slim

WORKDIR /app

# Copy everything in the data_ingestor directory into the container
COPY . .

# Install required packages
RUN pip install --no-cache-dir flask httpx pandas backoff tqdm
RUN pip install --no-cache-dir "httpx[http2]"
EXPOSE 5004

CMD ["python", "ingestor_service.py"]
