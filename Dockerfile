# Use the official Playwright image from Microsoft
# Playwright only supports till v1.48.0
# DO NOT UPGRADE TO v1.49.1
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/steam-stats
ENV HOME=/steam-stats

# Create a non-root user
RUN useradd -ms /bin/bash steam-stats

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
COPY assets/style.css /steam-stats/assets/

# Change ownership of the steam-stats directory to the non-root user
RUN chown -R steam-stats:steam-stats /steam-stats

# Switch to the non-root user
USER steam-stats

# Command to run the application
ENTRYPOINT ["sh", "-c", "cd /steam-stats && python -m api.main"]
