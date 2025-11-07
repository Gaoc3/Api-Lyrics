FROM python:3.11-slim

WORKDIR /app
COPY proj/ .
RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8080", "proj.app:app"]
