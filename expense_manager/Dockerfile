# Dockerfile (multi-stage build)
# Builder stage – install dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

# Runtime stage – copy only necessary files
FROM python:3.12-slim
WORKDIR /app
# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
# Copy application code
COPY . .
# Expose Flask default port
EXPOSE 5000
# Set environment variables for Flask
ENV FLASK_APP=run.py
# Use gunicorn in production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]