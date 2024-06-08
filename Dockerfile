# Use the official Python image from the Docker Hub
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /steam-stats

# Create the assets directory
RUN mkdir -p /steam-stats/assets

# Copy the requirements file into the container
ADD requirements.txt /steam-stats/requirements.txt

# Install dependencies and clean up
RUN apk add --no-cache \
	gcc \
	g++ \
	musl-dev \
	libffi-dev \
	libpng-dev \
	jpeg-dev \
	zlib-dev \
	libjpeg \
	make \
	git \
	firefox \
	&& pip install --no-cache-dir -r /steam-stats/requirements.txt \
	&& apk del gcc g++ musl-dev libffi-dev make \
	&& rm -rf /var/cache/apk/*

# Configure git
RUN git config --global user.email "action@github.com"
RUN git config --global user.name "GitHub Action"

ADD api/ ./api/
ADD assets/ ./assets/
ADD README.md ./

# Command to run the application
CMD ["python", "api/main.py"]
