# Use the official Python image with version 3.11.5
FROM python:3.11.5-slim

# Install PostgreSQL client and Alembic
RUN apt-get update && apt-get install -y \
    build-essential \        
    postgresql-client \
    libpq-dev \
    dos2unix \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir alembic grpcio psycopg2

# Set the working directory inside the container
WORKDIR /

# Install curl to download the wait-for-it.sh script
RUN apt-get update && apt-get install -y curl

# Download the wait-for-it.sh script
RUN curl -o /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it.sh

# Copy the requirements.txt file into the container
COPY ./requirements.txt /SRTFAKA/
COPY ./.env /SRTFAKA/
COPY ./alembic /SRTFAKA/alembic
COPY ./services /SRTFAKA/services
COPY ./alembic.ini /SRTFAKA/
COPY ./populate.sql /SRTFAKA/populate.sql

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r SRTFAKA/requirements.txt

# Copy the rest of the application code into the container
COPY ./apiGateway /SRTFAKA/apiGateway
COPY ./generated /SRTFAKA/generated
COPY ./common /SRTFAKA/common

RUN mv /SRTFAKA/apiGateway/entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 8000 for FastAPI (or other port if needed)
EXPOSE 80
