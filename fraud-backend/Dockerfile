# Use lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and model
COPY app.py .
COPY business_pipeline.pkl .

# Expose port 5000 for Flask
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
