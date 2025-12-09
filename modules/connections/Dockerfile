FROM python:3.10-slim

WORKDIR /app

COPY modules/connections /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "-u", "controller.py"]
