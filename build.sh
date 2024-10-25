#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Building Docker images with docker-compose..."
docker-compose build

echo "Starting Docker containers..."
docker-compose up -d

# Optional: Clean up dangling images to free up space
echo "Cleaning up dangling images..."
docker image prune -f

echo "Docker containers are now running."
