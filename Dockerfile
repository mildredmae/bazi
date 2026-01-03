# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port for FastAPI
EXPOSE 8001

# Start the FastAPI app
CMD ["uvicorn", "mcp_server:app", "--host", "0.0.0.0", "--port", "8001"]
