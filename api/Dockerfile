# استخدم بايثون الرسمي
FROM python:3.11-slim

WORKDIR /api

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8080", "index:app"]
