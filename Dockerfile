# Use the official Python image from the Docker Hub
FROM python:3.12.4-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /steam-stats

# Create the assets directory
RUN mkdir -p /steam-stats/assets

# Copy the requirements file into the container
COPY requirements.txt /steam-stats/requirements.txt

# Install Python dependencies and necessary tools, then clean up
RUN apt-get update && \
	apt-get install -y --no-install-recommends git && \
	pip install --no-cache-dir -r /steam-stats/requirements.txt && \
	pip install playwright && \
	playwright install --with-deps firefox --force && \
	git config --global user.email "action@github.com" && \
	git config --global user.name "GitHub Action" && \
	apt-get purge -y --auto-remove && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY api/* /steam-stats/api/
COPY README.md /steam-stats/

# Command to run the application
CMD ["python", "api/main.py"]
