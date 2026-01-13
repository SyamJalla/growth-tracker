# Docker Deployment Guide

This guide explains how to deploy Growth Tracker API using Docker.

## Quick Start

### 1. Prepare Configuration Files

```bash
cd Backend

# Copy config templates
cp config.ini.example config.ini
cp .env.docker .env

# Edit config.ini with your database credentials
# For Docker deployment, use 'db' as hostname (the service name)
```

**Update `config.ini` for Docker:**
```ini
[local]
database_url = postgresql+psycopg2://postgres:root@db:5432/growth_tracker
admin_database_url = postgresql+psycopg2://postgres:root@db:5432/postgres
```

### 2. Start Services

```bash
# Start all services (API + PostgreSQL)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (WARNING: deletes database data)
docker-compose down -v
```

### 3. Initialize Database

```bash
# Create database tables
curl -X POST http://localhost:8000/db/create_tables

# Check health
curl http://localhost:8000/api/health/db
```

## Docker Commands

### Build and Run

```bash
# Build image only
docker-compose build

# Start in foreground (see logs)
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up -d --build
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100
```

### Access Services

```bash
# API
curl http://localhost:8000

# API Documentation
# Open in browser: http://localhost:8000/docs

# PostgreSQL (from host)
psql -h localhost -U postgres -d growth_tracker
```

### Manage Services

```bash
# List running containers
docker-compose ps

# Stop services
docker-compose stop

# Start stopped services
docker-compose start

# Restart services
docker-compose restart

# Remove containers (keeps volumes)
docker-compose down

# Remove everything including volumes
docker-compose down -v
```

## Environment-Specific Deployment

### Local Development

```bash
# Use .env.local configuration
ENV=local docker-compose up -d
```

### Development Server

```bash
# Use .env.dev configuration
ENV=dev docker-compose up -d
```

### Production

```bash
# Use .env.prod configuration
ENV=prod docker-compose up -d
```

## Standalone Docker (Without Compose)

### Build Image

```bash
cd Backend
docker build -t growth-tracker-api .
```

### Run Container

```bash
# Basic run
docker run -d \
  -p 8000:8000 \
  -e ENV=local \
  -v $(pwd)/config.ini:/app/config.ini:ro \
  --name growth-tracker \
  growth-tracker-api

# With custom network and database
docker network create growth-network

docker run -d \
  --name postgres-db \
  --network growth-network \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=growth_tracker \
  postgres:15-alpine

docker run -d \
  -p 8000:8000 \
  --name growth-tracker \
  --network growth-network \
  -e ENV=local \
  -v $(pwd)/config.ini:/app/config.ini:ro \
  growth-tracker-api
```

## Configuration for Docker

### Database Connection

When running in Docker Compose, use the service name as hostname:

**config.ini:**
```ini
[local]
database_url = postgresql+psycopg2://postgres:root@db:5432/growth_tracker
admin_database_url = postgresql+psycopg2://postgres:root@db:5432/postgres
```

When connecting to external database:
```ini
[prod]
database_url = postgresql+psycopg2://user:pass@external-db.example.com:5432/growth_tracker
admin_database_url = postgresql+psycopg2://user:pass@external-db.example.com:5432/postgres
```

### Environment Variables

Docker Compose reads from `.env` file:

```env
ENV=local
POSTGRES_USER=postgres
POSTGRES_PASSWORD=root
POSTGRES_DB=growth_tracker
```

## Production Deployment

### 1. Security Checklist

- [ ] Use strong PostgreSQL passwords
- [ ] Don't expose PostgreSQL port (remove `ports` from db service)
- [ ] Use Docker secrets for sensitive data
- [ ] Enable SSL for database connections
- [ ] Restrict CORS origins in `.env.prod`
- [ ] Use read-only volume mounts

### 2. Production docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    environment:
      - ENV=prod
    volumes:
      - ./config.ini:/app/config.ini:ro
      - ./.env.prod:/app/.env.prod:ro
    secrets:
      - db_password
    restart: always
    
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: growth_tracker
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups:rw
    restart: always
    # Don't expose port in production

secrets:
  db_password:
    file: ./secrets/db_password.txt

volumes:
  postgres_data:
```

### 3. Backup Database

```bash
# Backup
docker-compose exec db pg_dump -U postgres growth_tracker > backup.sql

# Restore
docker-compose exec -T db psql -U postgres growth_tracker < backup.sql
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs api

# Common issues:
# - config.ini not found: Create from config.ini.example
# - Database connection failed: Check db service is running
# - Port already in use: Change port in docker-compose.yml
```

### Database connection refused

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker-compose exec db psql -U postgres -d growth_tracker
```

### Can't access API

```bash
# Check API is running
docker-compose ps api

# Check port mapping
docker port growth-tracker-api

# Check from inside container
docker-compose exec api curl localhost:8000/api/health/
```

### Reset Everything

```bash
# Stop and remove everything
docker-compose down -v

# Remove images
docker rmi growth-tracker-api postgres:15-alpine

# Start fresh
docker-compose up -d --build
```

## Monitoring

### Check Resource Usage

```bash
docker stats growth-tracker-api
docker stats growth-tracker-db
```

### Health Checks

```bash
# API health
curl http://localhost:8000/api/health/

# Database health
curl http://localhost:8000/api/health/db

# Container health
docker inspect --format='{{.State.Health.Status}}' growth-tracker-api
```

## Best Practices

1. **Always use volumes for database data**
2. **Mount config.ini as read-only**
3. **Use specific environment variables**
4. **Regular database backups**
5. **Monitor logs and resource usage**
6. **Use Docker secrets in production**
7. **Keep images updated**
8. **Don't store secrets in docker-compose.yml**

## Support

For Docker-specific issues:
- Check logs: `docker-compose logs`
- Review this guide
- Check Docker documentation
- Open an issue on GitHub
