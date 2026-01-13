# Growth Tracker Backend

Simple FastAPI backend for the Growth Tracker app.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the app with uvicorn:

```bash
uvicorn Backend.app:app --reload --host 0.0.0.0 --port 8000
```

3. Open the interactive docs at http://localhost:8000/docs

API routes

- `GET /api/smoking/` — list smoking entries
- `POST /api/smoking/` — create smoking entry
- `GET /api/smoking/{id}` — get smoking entry
- `PUT /api/smoking/{id}` — update smoking entry
- `DELETE /api/smoking/{id}` — delete smoking entry

- `GET /api/workouts/` — list workouts
- `POST /api/workouts/` — create workout
- `GET /api/workouts/{id}` — get workout
- `PUT /api/workouts/{id}` — update workout
- `DELETE /api/workouts/{id}` — delete workout

PostgreSQL setup

By default the project is configured to use PostgreSQL. Update the database URL via environment variable or `.env` file. Example `.env`:

```
DATABASE_URL=postgresql+psycopg2://postgres:root@localhost:5432/growth_tracker
```

To create the database locally (Postgres must be installed) you can run the new API endpoint `POST /db/create_database` with `{"db_name":"growth_tracker"}` or run:

```bash
createdb -U postgres growth_tracker
```

To create the tables in the configured database call the API endpoint `POST /db/create_tables` (or call `init_db()` from a script). Note: protect these endpoints in production.
