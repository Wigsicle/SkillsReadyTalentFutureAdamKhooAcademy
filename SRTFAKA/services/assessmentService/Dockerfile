# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file from the SRTFAKA folder to the container
COPY ../../requirements.txt .  

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade pip

# Copy the entire service code to the container
COPY . .

# Expose the port that the service will run on
EXPOSE 50053

# Command to run the service
CMD ["python", "-m", "services.assessmentService.main"]