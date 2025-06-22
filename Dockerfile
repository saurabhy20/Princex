# Dockerfile for Prince-X Userbot
FROM python:3.10-slim-bullseye

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "main.py"]
