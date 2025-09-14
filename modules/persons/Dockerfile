FROM python:3.10-slim

WORKDIR /app

COPY . /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "-u", "controller.py"]
