FROM python:3.11-slim

# Install system dependencies for wkhtmltopdf, pdf, images, etc
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    wget \
    libxrender1 \
    libfontconfig1 \
    libx11-6 \
    libxcb1 \
    libxext6 \
    xvfb \
    libssl-dev \
    poppler-utils \
    wkhtmltopdf \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

ENV FLASK_ENV=production

# Expose port used by Render
EXPOSE 5002

# Production server
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "dashboard:app", "--workers", "3", "--timeout", "120"]
