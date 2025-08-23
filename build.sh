#!/bin/bash

# Exit on any error
set -e

# Build the frontend
cd frontend
npm install
npm run build
cd ..

# Install backend dependencies
pip install -r backend/requirements.txt
