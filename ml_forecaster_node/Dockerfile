FROM python:3.10-slim

WORKDIR /app

COPY forecast_service.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5011

CMD ["python", "forecast_service.py"]