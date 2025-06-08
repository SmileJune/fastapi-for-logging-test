# Use Python 3.12 slim image with specific SHA256
FROM python@sha256:0175d8ff0ad1dc8ceca4bcf311c3e47d08807a940959fa1cdbcefa87841883a1

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN addgroup --system appuser && adduser --system --ingroup appuser appuser
USER appuser

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 