FROM python:3.12-slim

WORKDIR /app

COPY smart_agent_service.py /app/

# 🆕 Install all required packages
RUN pip install flask requests flask_cors

CMD ["python", "smart_agent_service.py"]