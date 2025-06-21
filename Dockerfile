FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Копируем SSL сертификаты (если используем свои)
# COPY ssl/ /etc/ssl/

CMD ["python", "webhook-server/webhook.py"]