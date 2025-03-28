FROM python:3.12-slim

WORKDIR /app

COPY anomaly_service.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "anomaly_service.py"]
