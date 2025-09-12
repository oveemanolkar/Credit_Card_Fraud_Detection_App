# Use slim Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY business_pipeline.pkl .

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
