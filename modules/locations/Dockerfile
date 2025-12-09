FROM python:3.10-slim

WORKDIR /app

COPY modules/locations /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "-u", "controller.py"]
