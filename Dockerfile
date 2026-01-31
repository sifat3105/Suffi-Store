# -----------------------------------------
# Base Image
# -----------------------------------------
FROM python:3.11-slim



# Set working directory
WORKDIR /app

# System dependencies (for psycopg2, Pillow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire Django project
COPY . .

# Copy entrypoint script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Create a non-root user and switch
RUN useradd -ms /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

# Expose internal port
EXPOSE 8000

# Collect static files (optional)
# If you want automatic collectstatic, uncomment this.
RUN python manage.py collectstatic --noinput

# Entrypoint (runs migrations + collectstatic + gunicorn)
ENTRYPOINT ["/app/entrypoint.sh"]
