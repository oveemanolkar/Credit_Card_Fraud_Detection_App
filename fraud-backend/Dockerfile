# Use official Python runtime
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY business_pipeline.pkl .
COPY creditcard.csv .   # optional: only if your pipeline needs it at runtime

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
