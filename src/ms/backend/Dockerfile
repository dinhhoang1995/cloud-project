# Use an official Python runtime as a parent image
FROM python:3-slim

# copy only the requirements.txt file at first
COPY requirements.txt /backend_service/

# Set the working directory to /app
WORKDIR /backend_service

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /backend_service

# Make port 8080 available to the world outside this container
EXPOSE 8070

# Run app.py when the container launches
CMD ["python3", "backend_service_main.py"]
