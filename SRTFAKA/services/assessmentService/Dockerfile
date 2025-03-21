# Use the official Python image with version 3.11.5
FROM python:3.11.5-slim

# Install PostgreSQL client and Alembic
RUN apt-get update && apt-get install -y \
    build-essential \        
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir alembic grpcio psycopg2

# Set the working directory inside the container
WORKDIR /SRTFAKA

# Copy the requirements.txt file into the container
COPY ./requirements.txt /SRTFAKA/

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./services/assessmentService /SRTFAKA/services/assessmentService
COPY ./generated /SRTFAKA/generated
COPY ./apiGateway/base.py /SRTFAKA/apiGateway/base.py
COPY ./common /SRTFAKA/common


# Expose port 8000 for FastAPI (or other port if needed)
EXPOSE 50053

# Default command to run the application (adjust based on service)
CMD ["python", "-m", "services.assessmentService.main"]
