#!/bin/bash
echo "Starting Odoo 17 development environment..."
docker-compose --profile odoo17 up -d
echo "Odoo 17 is running on http://localhost:8069"
echo "Database: Use 'db' as hostname, 'odoo' as user and password"
