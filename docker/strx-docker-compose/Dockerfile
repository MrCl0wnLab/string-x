# Use Python 3.12 Alpine for modern String-X requirements
FROM python:3.12-alpine3.21

# Adicionar metadados como labels
LABEL maintainer="MrCl0wn <mrcl0wnlab[@]gmail.com>"
LABEL version="1.0.0"
LABEL description="String-X: Modern OSINT Automation Tool with Python 3.12+"
LABEL org.opencontainers.image.source="https://github.com/MrCl0wnLab/string-x"
LABEL org.opencontainers.image.title="String-X"
LABEL org.opencontainers.image.description="Fast and customizable automation tool for string manipulation and OSINT"
LABEL org.opencontainers.image.licenses="MIT"

# Install system dependencies
RUN apk add --no-cache \
    git \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    curl \
    wget \
    nmap \
    bind-tools \
    whois \
    && rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -e .

# Create non-root user for security
RUN addgroup -g 1000 strx && \
    adduser -D -s /bin/sh -u 1000 -G strx strx

# Create directories and set permissions
RUN mkdir -p /app/data /app/output && \
    chown -R strx:strx /app

# Switch to non-root user
USER strx

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD strx -h > /dev/null || exit 1

# Default entrypoint and command
ENTRYPOINT ["strx"]
CMD ["-examples"]