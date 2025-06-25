# Odoo Development Environment

This Docker Compose setup provides both Odoo 17 and Odoo 18 development environments.

## Services

### Databases

- **db17**: PostgreSQL 17 for Odoo 17 (port 5432)
- **db18**: PostgreSQL 17 for Odoo 18 (port 5433)

### Odoo Instances

- **odoo17**: Odoo 17 instance (port 8070)
- **odoo18**: Odoo 18 instance (port 8069)

## Usage

### Start the services

```bash
docker-compose up -d
```

### Access the applications

- Odoo 17: <http://localhost:8070>
- Odoo 18: <http://localhost:8069>

### Stop the services

```bash
docker-compose down
```

### View logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f odoo17
docker-compose logs -f odoo18
```

## Configuration

### Database Configuration

- Odoo 17 uses database `odoo17` with user `odoo17`
- Odoo 18 uses database `odoo18` with user `odoo18`
- Both databases use the same password as their respective usernames

### Addons

- Odoo 17 addons: `./addons/odoo17/`
- Odoo 18 addons: `./addons/odoo18/`

### Data Persistence

- Odoo 17 database data: `./data/db/`
- Odoo 18 database data: Docker volume `odoo18-db-data`

## Development

Place your custom addons in the respective addon directories:

- For Odoo 17: `addons/odoo17/`
- For Odoo 18: `addons/odoo18/`

The containers will automatically detect and load addons from these directories.
