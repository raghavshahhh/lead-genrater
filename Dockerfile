FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    wget \
    curl \
    fontconfig \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    xfonts-75dpi \
    xfonts-base \
 && rm -rf /var/lib/apt/lists/*

# Install wkhtmltopdf manually (not available in Debian Trixie repos)
RUN wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
 && apt-get update \
 && apt-get install -y --no-install-recommends ./wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
 && rm wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

# Create necessary directories (if they don't exist from COPY)
RUN mkdir -p /app/data /app/data/history /app/data/backups /app/logs

# Note: data/ and config/ folders are already copied by "COPY . /app" above
# This includes:
# - data/premium_leads.json (529 leads)
# - config/settings.json (API keys)

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5002/api/stats', timeout=5)"

# Expose port used by Render
EXPOSE 5002

# Production server with optimized settings
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "dashboard:app", \
     "--workers", "3", \
     "--threads", "2", \
     "--timeout", "120", \
     "--keep-alive", "5", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
