# Growth Tracker

A complete full-stack application for tracking personal growth metrics including workout sessions and smoking habits. Features a FastAPI backend with PostgreSQL database and a React Native mobile frontend.

## 🚀 Features

### Backend (FastAPI)
- ✅ RESTful API with FastAPI
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Workout tracker with streak calculations
- ✅ Smoking tracker with relapse monitoring
- ✅ Dashboard with comprehensive KPIs
- ✅ Health check endpoints (app & database)
- ✅ Comprehensive API documentation
- ✅ Docker support with docker-compose
- ✅ Environment-based configuration
- ✅ Automated testing (84% coverage)
- ✅ CORS enabled

### Frontend (React Native)
- ✅ Cross-platform mobile app (iOS, Android, Web)
- ✅ Material Design UI with React Native Paper
- ✅ Dashboard with KPIs and charts
- ✅ Workout logging and tracking
- ✅ Smoking entry tracking with streaks
- ✅ Health status monitoring
- ✅ Pull-to-refresh functionality
- ✅ Form validation and error handling
- ✅ Full backend API integration

## 📋 Prerequisites

### Backend
- Python 3.8+
- PostgreSQL 12+
- pip package manager

### Frontend
- Node.js 14+
- npm or yarn
- Expo CLI (optional, for development)

## 🛠️ Installation

### Clone the repository

```bash
git clone https://github.com/SyamJalla/growth-tracker.git
cd growth-tracker
```

---

## Backend Setup

### 1. Navigate to Backend directory

```bash
cd Backend
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

Create configuration files in the `Backend` directory:

**config.ini:**
```ini
[database]
user = postgres
password = root
host = localhost
port = 5432
database = growth_tracker
```

**Configuration details:** See [Backend/CONFIGURATION.md](Backend/CONFIGURATION.md)

### 5. Start the server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

---

## Frontend Setup

### 1. Navigate to Frontend directory

```bash
cd Frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure API URL

Edit `src/services/config.js` and set the appropriate API URL:

```javascript
export const API_CONFIG = {
  LOCAL: 'http://localhost:8000/api',
  PRODUCTION: 'https://your-api-url.com/api',
};

export const CURRENT_ENV = 'LOCAL';
```

### 4. Start the app

```bash
npm start
```

Then choose your platform:
- Press `i` for iOS Simulator (Mac only)
- Press `a` for Android Emulator
- Press `w` for Web Browser
PI Endpoints

### Health Check
- `GET /api/health` - Check application health
- `GET /api/health/db` - Check database connectivity

### Dashboard
- `GET /api/dashboard/kpis` - Get all KPIs
- `GET /api/dashboard/weekly-progress` - Get weekly workout progress
- `GET /api/dashboard/trends` - Get monthly trends

### Workout Tracker
- `POST /api/workouts` - Log new workout
- `GET /api/workouts` - Get all workouts
- `GET /api/workouts/{id}` - Get specific workout
- `PUT /api/workouts/{id}` - Update workout
- `DELETE /api/workouts/{id}` - Delete workout
- `GET /api/workouts/stats/weekly` - Weekly workout stats
- `GET /api/workouts/stats/monthly` - Monthly workout stats

### Smoking Tracker
- `POST /api/smoking` - Log smoking entry
- `GET /api/smoking` - Get all entries
- `GET /api/smoking/{id}` - Get specific entry
- `DELETE /api/smoking/{id}` - Delete entry
- `GET /api/smoking/stats/weekly` - Weekly smoking stats
- `GET /api/smoking/stats/monthly` - Monthly smoking stats
- `GET /api/smoking/stats/streak` - Get streak information

### Database Tasks
- `DELETE /api/db/clear` - Clear all data
- `GET /api/db/export` - Export data
- `POST /api/db/import` - Import data

**Full API Documentation:** [Backend/api-docs/](Backend/api-docs/)
```

The API will be available at: **http://localhost:8000**

**Docker details:** See [Backend/DOCKER.md](Backend/DOCKER.md)

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

### � Mobile App Features

### Dashboard Screen
- KPI cards (workout streak, smoke-free days, total workouts, average duration)
- Weekly workout progress chart
- Monthly trends display
- Pull-to-refresh

### Workout Tracker
- Log workouts with type, duration, intensity, calories
- Edit and delete entries
- Weekly statistics
- History view

### Smoking Tracker
- Log smoking entries with cigarette count
- Track mood and triggers
- View current and longest streak
- Weekly statistics

### Health Status
### Backend Tests

Run tests using pytest:

```bash
cd Backend
pytest tests/
```

**Test Coverage:** 84% (48/52 tests passing)

**Test Results:** See [Backend/tests/TEST_RESULTS.md](Backend/tests/TEST_RESULTS.md)POST /db/create_database` - Create new database
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
                          # FastAPI Backend
│   ├── api/                          # API route handlers
│   │   ├── dashboard.py              # Dashboard KPIs endpoint
│   │   ├── workout_tracker.py        # Workout CRUD operations
│   │   ├── smoking_tracker.py        # Smoking CRUD operations
│   │   ├── health.py                 # Health check endpoints
│   │   └── db_tasks.py               # Database utilities
│   ├── core/                         # Core configuration
│   │   ├── settings.py               # Settings and config loader
│   │   └── logging_config.py         # Logging configuration
│   ├── db/                           # Database layer
│   │   ├── database.py               # Database connection
│   │   ├── models.py                 # SQLAlchemy models
│   │   └── __init__.py
│   ├── api-docs/                     # API documentation
│   │   ├── API-Documentation.md      # Markdown docs
│   │   ├── API-Documentation.html    # HTML docs
│   │   ├── growth-tracker.postman_collection.json
│   │   └── README.md
│   ├── tests/                        # Test suite (pytest)
│   │   ├── conftest.py               # Test fixtures
│   │   ├── test_app.py
│   │   ├── test_dashboard.py
│   │   ├── test_workout_tracker.py
│   │   ├── test_smoking_tracker.py
│   │   ├── test_kpi_calculations.py
│   │   ├── test_models_db.py
│   │   ├── README.md
│   │   └── TEST_RESULTS.md
│   ├── app.py                        # Main application
│   ├── config.ini.example            # Example config file
│   ├── .env.example                  # Example environment file
│   ├── Dockerfile                    # Docker configuration
│   ├── docker-compose.yml            # Docker Compose setup
│   ├── requirements.txt              # Python dependencies
│   ├── pytest.ini                    # Pytest configuration
### Backend Configuration

Configuration is managed through `config.ini` and environment variables:

**config.ini:**
```ini
[database]
user = postgres
password = your_password
host = localhost
port = 5432
database = growth_tracker
```

**Environment Variables:**
- `ENV` - Environment (local/dev/prod)
- `APP_NAME` - Application name
- `CORS_ORIGINS` - Allowed CORS origins

See [Backend/CONFIGURATION.md](Backend/CONFIGURATION.md) for detailed configuration guide.

### Frontend Configuration

Update API URL in `Frontend/src/services/config.js`:

```✅ Completed Features

- ✅ Workout tracker with full CRUD operations
- ✅ Smoking tracker with streak calculations
- ✅ Dashboard with comprehensive KPIs
- ✅ Backend API with FastAPI + PostgreSQL
- ✅ React Native mobile frontend
- ✅ Docker support with docker-compose
- ✅ Comprehensive API documentation
- ✅ Automated testing suite (84% coverage)
- ✅ Material Design UI
- ✅ Data visualization with charts
- ✅ Pull-to-refresh functionality
- ✅ Form validation and error handling

## 🚧 Future Enhancements

### Backend
- [ ] User authentication and authorization
- [ ] Multi-year tracking support
- [ ] Advanced analytics and insights
- [ ] API rate limiting
- [ ] WebSocket support for real-time updates
- [ ] Set up CI/CD pipeline

### Frontend
- [ ] Offline support with local caching
- [ ] Push notifications for reminders
- [ ] Dark mode theme
- [ ] Advanced charts (bar, pie, trend lines)
- [ �️ Technology Stack

### Backend
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Testing:** pytest
- **Deployment:** Docker, docker-compose

### Frontend
- **Framework:** React Native with Expo
- **UI Library:** React Native Paper (Material Design)
- **Navigation:** React Navigation
- **HTTP Client:** Axios
- **Charts:** React Native Chart Kit
- **Storage:** AsyncStorage

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Check the [API documentation](Backend/api-docs/)
- Review the interactive docs at http://localhost:8000/docs
- Frontend guide: [Frontend/README.md](Frontend/README.md)
- Backend configuration: [Backend/CONFIGURATION.md](Backend/CONFIGURATION.md)
- Docker guide: [Backend/DOCKER.md](Backend/DOCKER.md)

---

**Made with ❤️ using FastAPI and React Nativeodal.js
│   │   │   └── SmokingFormModal.js
│   │   └── services/
│   │       ├── api.js                # API client
│   │       └── config.js             # API configuration
│   ├── App.js                        # Root component
│   ├── package.json                  # Node dependencies
│   ├── app.json                      # Expo configuration
│   ├── babel.config.js
│   └── README.md                     # Frontend guide
│
├── planning/                         # Project planning
│   ├── plan.txt                      # Requirements & versions
│   ├── plan.jpeg                     # Original plan
│   └── prompt-history.md             # Development history
│
├── .gitignore
└── README.md            ocs/         # API documentation
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
