FROM python:3.11-slim AS builder

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



FROM python:3.11-slim

WORKDIR /ml_module


COPY --from=builder /opt/venv /opt/venv


ENV PATH="/opt/venv/bin:$PATH"


COPY . .

EXPOSE 5000

CMD ["python", "main.py"]