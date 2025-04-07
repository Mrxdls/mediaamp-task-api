# Dockerfile

FROM python:3.12-slim

# Set working directory
WORKDIR /Mediaamp

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev && \
    apt-get clean

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY APP ./APP
COPY run.py ./run.py

# Expose the Flask port
EXPOSE 5000

# Start the app
CMD ["python3", "run.py"]
