# Use the official Playwright image from the Docker Hub
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /steam-stats

# Create the assets directory
RUN mkdir -p /steam-stats/assets

# Copy the requirements file into the container
COPY requirements.txt /steam-stats/requirements.txt

# Install Python dependencies and necessary tools
RUN apt-get update && \
	apt-get install -y --no-install-recommends git && \
	pip install --no-cache-dir -r /steam-stats/requirements.txt && \
	apt-get purge -y --auto-remove && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy application code and other necessary files into the container
COPY api/ /steam-stats/api/
COPY README.md /steam-stats/

# Command to run the application
CMD ["python", "api/main.py"]
