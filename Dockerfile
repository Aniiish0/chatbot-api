# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install build dependencies
RUN apk add --no-cache gcc g++ musl-dev libffi-dev openssl-dev make

# Install any needed packages specified in requirements.txt
RUN pip --version
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV APP_PORT=5000

# Feed the knowledge base and run the application
CMD ["sh", "-c", "python helpers/feed_or_search.py $INPUT_PATH && flask run --host=0.0.0.0 --port=$APP_PORT"]
