FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for numpy, pandas, PIL, etc.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        gcc \
        git \
        wget \
        curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for UTF-8 and production
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port for Hugging Face Spaces
EXPOSE 7860

# Healthcheck (optional, but recommended for cloud)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:7860/docs || exit 1

# Use python -m uvicorn for reliability
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]