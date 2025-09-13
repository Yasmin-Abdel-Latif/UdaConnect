# modules/api-gateway/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# deps
COPY modules/api-gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app code
COPY modules/api-gateway/controller.py /app/

# make the Python package layout explicit
RUN mkdir -p /app/modules/connections \
 && : > /app/modules/__init__.py \
 && : > /app/modules/connections/__init__.py

# bring in ONLY the generated gRPC stubs from the connections service
# (these files already exist in your repo)
COPY modules/connections/location_connection_pb2.py /app/modules/connections/location_connection_pb2.py
COPY modules/connections/location_connection_pb2_grpc.py /app/modules/connections/location_connection_pb2_grpc.py

# (optional) if you have any local helpers under modules/api-gateway/modules, copy them too
# this will overlay without removing what we created above
COPY modules/api-gateway/modules/ /app/modules/

ENV PYTHONPATH=/app
EXPOSE 5002
CMD ["python", "controller.py"]
