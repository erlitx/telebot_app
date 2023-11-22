# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY .env /app
COPY logger.py /app
COPY odoo_api.py /app
COPY telebot_app.py /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Start telebot_app.py when the container launches
CMD ["python", "telebot_app.py"]
