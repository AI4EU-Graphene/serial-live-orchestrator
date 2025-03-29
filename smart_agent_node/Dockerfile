FROM python:3.12-slim

WORKDIR /app
COPY smart_agent_service.py /app/

RUN pip install flask requests

EXPOSE 5013
CMD ["python", "smart_agent_service.py"]