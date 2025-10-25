FROM python:3.9-slim

WORKDIR /workspace

COPY requirements.txt /workspace/cli/requirements.txt
RUN pip install --no-cache-dir -r /workspace/cli/requirements.txt

COPY .. /workspace

# Default to gutil codex-repl; can override with `docker run ... python -m gutil -h`
CMD ["python", "-m", "gutil", "codex-repl"]
