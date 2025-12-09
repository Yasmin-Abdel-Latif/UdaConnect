#!/bin/bash
set -e
export PYTHONPATH=/app:${PYTHONPATH}
exec python -u /app/controller.py "$@"
