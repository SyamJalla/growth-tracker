# Configuration Guide

This guide explains how to configure the Growth Tracker API for different environments.

## Configuration Files

### 1. Environment Files (.env)

Environment-specific settings are stored in `.env` files:

- **`.env.local`** - Local development
- **`.env.dev`** - Development environment
- **`.env.prod`** - Production environment
- **`.env.example`** - Template file (tracked in git)

### 2. Database Configuration (config.ini)

Database connection strings for all environments are stored in `config.ini`:

- **`config.ini`** - Actual database credentials (NOT tracked in git)
- **`config.ini.example`** - Template file (tracked in git)

## Setup Instructions

### First Time Setup

1. **Copy the example files:**

   ```bash
   cd Backend
   
   # Copy environment template
   cp .env.example .env.local
   
   # Copy database config template
   cp config.ini.example config.ini
   ```

2. **Edit `config.ini` with your actual database credentials:**

   ```ini
   [local]
   database_url = postgresql+psycopg2://your_user:your_password@localhost:5432/growth_tracker
   admin_database_url = postgresql+psycopg2://your_user:your_password@localhost:5432/postgres
   ```

3. **Edit `.env.local` if needed:**

   ```env
   APP_NAME=Growth Tracker API
   ENV=local
   CORS_ORIGINS=["http://localhost:3000"]
   ```

### How It Works

1. **Environment Selection:**
   - Set `ENV` variable in your `.env` file (local/dev/prod)
   - Or set as system environment variable: `export ENV=dev`

2. **Automatic Loading:**
   - Application reads `ENV` variable
   - Loads corresponding `.env.{ENV}` file (e.g., `.env.local`)
   - Reads database config from `config.ini` using the `[ENV]` section

3. **Priority Order:**
   - `.env.{ENV}` (e.g., `.env.local`)
   - `.env.local` (fallback)
   - `.env` (fallback)

## Environment Variables

### Application Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | "Growth Tracker API" | Application name |
| `ENV` | "local" | Environment: local, dev, or prod |
| `CORS_ORIGINS` | ["*"] | Allowed CORS origins (JSON array) |

### Mail Settings (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `MAIL_USERNAME` | None | Email username for sending emails |
| `MAIL_PASSWORD` | None | Email password |
| `MAIL_FROM` | "noreply@example.com" | From email address |
| `MAIL_SERVER` | None | SMTP server address |
| `MAIL_PORT` | 587 | SMTP server port |

### Database Settings (from config.ini)

Database URLs are automatically loaded based on the `ENV` setting:

- `database_url` - Main application database
- `admin_database_url` - Admin database for creating databases

## Examples

### Local Development

**`.env.local`:**
```env
APP_NAME=Growth Tracker API
ENV=local
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

**`config.ini` [local] section:**
```ini
[local]
database_url = postgresql+psycopg2://postgres:root@localhost:5432/growth_tracker
admin_database_url = postgresql+psycopg2://postgres:root@localhost:5432/postgres
```

### Development Server

**`.env.dev`:**
```env
APP_NAME=Growth Tracker API - Dev
ENV=dev
CORS_ORIGINS=["https://dev.yourdomain.com"]
MAIL_USERNAME=dev@example.com
MAIL_PASSWORD=dev_password
```

**`config.ini` [dev] section:**
```ini
[dev]
database_url = postgresql+psycopg2://devuser:devpass@dev-db.example.com:5432/growth_tracker_dev
admin_database_url = postgresql+psycopg2://devuser:devpass@dev-db.example.com:5432/postgres
```

### Production

**`.env.prod`:**
```env
APP_NAME=Growth Tracker API
ENV=prod
CORS_ORIGINS=["https://yourdomain.com"]
MAIL_USERNAME=noreply@yourdomain.com
MAIL_PASSWORD=secure_password
```

**`config.ini` [prod] section:**
```ini
[prod]
database_url = postgresql+psycopg2://produser:secure_pass@prod-db.example.com:5432/growth_tracker
admin_database_url = postgresql+psycopg2://produser:secure_pass@prod-db.example.com:5432/postgres
```

## Running with Different Environments

### Method 1: Using Environment Variable

```bash
# Linux/Mac
export ENV=dev
uvicorn app:app --reload

# Windows CMD
set ENV=dev
uvicorn app:app --reload

# Windows PowerShell
$env:ENV="dev"
uvicorn app:app --reload
```

### Method 2: Using .env File

Just make sure your `.env.{ENV}` file has the correct `ENV` value:

```env
ENV=dev
```

Then run normally:
```bash
uvicorn app:app --reload
```

## Security Best Practices

### ✅ DO:
- Keep `config.ini` and `.env.local` in `.gitignore`
- Use strong passwords in production
- Use environment variables in CI/CD pipelines
- Rotate credentials regularly
- Use different credentials for each environment

### ❌ DON'T:
- Commit actual credentials to git
- Share production credentials
- Use the same password across environments
- Store credentials in code files

## Troubleshooting

### Config file not found

**Error:** `config.ini not found`

**Solution:** Copy the example file:
```bash
cp config.ini.example config.ini
```

### Wrong environment loaded

**Check:**
1. Value of `ENV` in your `.env` file
2. System environment variable `ENV`
3. Config.ini has the corresponding `[env]` section

### Database connection failed

**Check:**
1. Database credentials in `config.ini`
2. Database server is running
3. Network connectivity to database
4. Correct `ENV` section in `config.ini`

## Migration from Old Setup

If you were using the old configuration:

1. **Backup your old `.env` file**
2. **Create `config.ini`** and move database URLs there
3. **Create `.env.local`** with non-database settings
4. **Update your deployment scripts** to use the new structure

## Support

For issues with configuration:
- Check this guide
- Review `config.ini.example` and `.env.example`
- Open an issue on GitHub
