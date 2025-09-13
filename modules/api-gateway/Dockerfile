# modules/api-gateway/Dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

WORKDIR /app

# 1) Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) App sources
COPY controller.py .
COPY modules/ ./modules/

# 3) Make sure Python packages exist (handles missing __init__.py files)
RUN python - <<'PY'
import pathlib
for pkg in ("modules", "modules/connections"):
    p = pathlib.Path(pkg) / "__init__.py"
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("")
PY

# 4) OPTIONAL: compile any *.proto found under modules/ if they exist
# (No error if none are present.)
RUN set -e; \
  if find modules -type f -name '*.proto' -print -quit | grep -q .; then \
    pip install --no-cache-dir grpcio grpcio-tools; \
    for f in $(find modules -type f -name '*.proto'); do \
      d="$(dirname "$f")"; \
      python -m grpc_tools.protoc -I"$d" -Imodules \
        --python_out="$d" --grpc_python_out="$d" "$f"; \
    done; \
  fi

# 5) Default command
CMD ["python", "controller.py"]
