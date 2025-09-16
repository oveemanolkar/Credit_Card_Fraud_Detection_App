# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY business_pipeline.pkl .

# Expose Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
