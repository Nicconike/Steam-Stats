# Use the official Playwright image from Microsoft with pinned digest
FROM mcr.microsoft.com/playwright/python:v1.61.0-jammy-amd64@sha256:85693c97d366771716f18deb969dad46198cdce998d734051fd3eb3e0b19a038

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONPATH=/steam-stats

# Create non-root user with explicit UID
RUN useradd -u 10000 -ms /bin/bash steam-stats

# Set the working directory
WORKDIR /steam-stats

# Copy project files
COPY . .

# Install necessary packages
RUN apt-get update && \
	apt-get install -y --no-install-recommends git && \
	pip install --no-cache-dir --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt && \
	pip install --no-cache-dir -e . && \
	apt-get purge -y --auto-remove git && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
	chown -R steam-stats:steam-stats /steam-stats/

# Switch to non-root user
USER steam-stats

# Command to run the application
ENTRYPOINT ["python", "-m", "api.main"]
