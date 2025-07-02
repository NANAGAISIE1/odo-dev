#!/bin/bash
echo "Starting Odoo 18 development environment..."
docker-compose --profile odoo18 up -d
echo "Odoo 18 is running on http://localhost:8070"
echo "Database: Use 'odoo18_db' as hostname, 'odoo' as user and password"
