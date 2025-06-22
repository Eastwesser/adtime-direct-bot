FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
COPY packages/ /tmp/packages/

RUN pip install --no-cache-dir \
    --find-links=/tmp/packages/ \
    --retries 5 \
    -r requirements.txt

COPY . .

CMD ["python", "webhook-server/webhook.py"]