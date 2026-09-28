FROM python:3.12-slim

WORKDIR /app

COPY app.py .
COPY templates ./templates
COPY static ./static

EXPOSE 8000

CMD ["python", "app.py"]
