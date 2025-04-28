#!/bin/bash
echo "Running Database Migrations..."
flask db upgrade

echo "Starting Flask server..."
flask run --host=0.0.0.0 --port=5000
