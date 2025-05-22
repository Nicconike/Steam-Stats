# Use the official Playwright image from Microsoft with pinned digest
FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy-amd64@sha256:afdc65b821d031edc7853f7e267b33885a17e2763c6a49cbdbd8a831bdf130fd

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1

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
