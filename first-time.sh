#!/bin/bash

# This script sets up the environment for the Vibe Coding Template project.
# It installs necessary dependencies and prepares the project for development.

# Navigate to the backend directory and install dependencies
echo "Setting up backend..."
cd backend
pip install -r requirements.txt

# Navigate to the CLI directory and install dependencies
echo "Setting up CLI..."
cd ../cli
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
cd ../supabase/migrations
# Assuming a command to run migrations exists, replace with actual command if needed
# e.g., supabase db push or similar command

# Return to the project root
cd ../../

echo "Setup complete! You can now start the development server using 'make dev'."