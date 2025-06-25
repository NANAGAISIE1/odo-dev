#!/bin/bash
echo "Starting development tools (pgAdmin)..."
docker-compose --profile tools up -d
echo "pgAdmin is running on http://localhost:5050"
echo "Login: admin@example.com / admin"
