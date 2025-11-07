# Use lightweight Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies from proj/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the default port (Fly.io uses 8080)
ENV PORT=8080

# Run the Flask app from proj/app.py
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
