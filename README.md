# Growth Tracker

A FastAPI-based backend service for tracking personal growth metrics including health monitoring and database management utilities.

## 🚀 Features

- ✅ RESTful API with FastAPI
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Health check endpoints (app & database)
- ✅ Database initialization utilities
- ✅ Comprehensive API documentation
- ✅ Docker support
- ✅ CORS enabled
- 🔄 Smoking tracker (planned)
- 🔄 Workout tracker (planned)

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip package manager

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/SyamJalla/growth-tracker.git
cd growth-tracker/Backend
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

**Windows:**
```bash
.\.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Create a `.env` file in the `Backend` directory:

```env
APP_NAME=Growth Tracker API
ENV=dev
DATABASE_URL=postgresql+psycopg2://postgres:root@localhost:5432/growth_tracker
ADMIN_DATABASE_URL=postgresql+psycopg2://postgres:root@localhost:5432/postgres
CORS_ORIGINS=["*"]
```

### 5. Start the server

```bash
cd Backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

## 🗄️ Database Setup

### Initialize Database

After starting the server, initialize the database using the API endpoints:

1. **Create Database:**
   ```bash
   curl -X POST http://localhost:8000/db/create_database \
     -H "Content-Type: application/json" \
     -d '{"db_name": "growth_tracker"}'
   ```

2. **Create Tables:**
   ```bash
   curl -X POST http://localhost:8000/db/create_tables
   ```

3. **Verify Database Connection:**
   ```bash
   curl http://localhost:8000/api/health/db
   ```

### Alternative: Manual Database Creation

```bash
# Using PostgreSQL command line
createdb -U postgres growth_tracker

# Or connect to postgres and run
CREATE DATABASE growth_tracker;
```

## 📚 API Documentation

### Interactive Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Comprehensive Documentation

Detailed API documentation is available in the `Backend/api-docs/` folder:

- **Markdown:** `API-Documentation.md`
- **HTML (Print to PDF):** `API-Documentation.html`
- **Postman Collection:** `growth-tracker.postman_collection.json`

See [Backend/api-docs/README.md](Backend/api-docs/README.md) for more information.

## 🔗 Available Endpoints

### Root
- `GET /` - API status

### Health Check
- `GET /api/health/` - Check application health
- `GET /api/health/db` - Check database connectivity

### Database Management
- `POST /db/create_database` - Create new database
- `POST /db/create_tables` - Initialize database tables

## 🐳 Docker Support

### Build the image

```bash
cd Backend
docker build -t growth-tracker-api .
```

### Run the container

```bash
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg2://user:password@host/dbname \
  --name growth-tracker \
  growth-tracker-api
```

## 🧪 Testing

Run tests using pytest:

```bash
cd Backend
pytest tests/
```

## 📁 Project Structure

```
growth-tracker/
├── Backend/
│   ├── api/              # API route handlers
│   │   ├── health.py     # Health check endpoints
│   │   ├── db_tasks.py   # Database utilities
│   │   ├── smoking_tracker.py
│   │   └── workout_tracker.py
│   ├── core/             # Settings and configuration
│   │   ├── settings.py
│   │   └── logging_config.py
│   ├── db/               # Database models and connection
│   │   ├── database.py
│   │   ├── models.py
│   │   └── __init__.py
│   ├── api-docs/         # API documentation
│   │   ├── API-Documentation.md
│   │   ├── API-Documentation.html
│   │   ├── growth-tracker.postman_collection.json
│   │   └── README.md
│   ├── scripts/          # Utility scripts
│   ├── tests/            # Test files
│   ├── app.py            # Main application
│   ├── Dockerfile
│   └── requirements.txt
├── planning/             # Project planning files
├── .gitignore
└── README.md             # This file
```

## ⚙️ Configuration

All configuration is managed through environment variables or `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | "Growth Tracker API" | Application name |
| `ENV` | "dev" | Environment (dev/staging/prod) |
| `DATABASE_URL` | `postgresql+psycopg2://postgres:root@localhost:5432/growth_tracker` | Main database connection |
| `ADMIN_DATABASE_URL` | `postgresql+psycopg2://postgres:root@localhost:5432/postgres` | Admin database connection |
| `CORS_ORIGINS` | ["*"] | Allowed CORS origins |

## 🔧 Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes

### Adding New Endpoints

1. Create route handler in `Backend/api/`
2. Update `Backend/app.py` to include the router
3. Update API documentation
4. Add tests in `Backend/tests/`

## 🚧 Roadmap

- [ ] Implement smoking tracker endpoints
- [ ] Implement workout tracker endpoints
- [ ] Add user authentication and authorization
- [ ] Add data visualization endpoints
- [ ] Implement data export functionality
- [ ] Add API rate limiting
- [ ] Set up CI/CD pipeline

## 📝 License

[Add your license information here]

## 👤 Author

**Syam Jalla**
- GitHub: [@SyamJalla](https://github.com/SyamJalla)
- Email: syamjalla@gmail.com

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Check the [API documentation](Backend/api-docs/)
- Review the interactive docs at `/docs`

---

**Made with ❤️ using FastAPI**
