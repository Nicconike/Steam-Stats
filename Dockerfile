# Use the official Playwright image from Microsoft with pinned digest
FROM mcr.microsoft.com/playwright/python:v1.59.0-jammy-amd64@sha256:d0c442885ef05512ce8c6a273c3eb9d247d8f0cfdf64ab0d05503172b3d79c3c

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
