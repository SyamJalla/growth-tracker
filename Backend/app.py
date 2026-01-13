from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from core.settings import Settings
from core.logging_config import setup_logging
from db.database import init_db

from api.smoking_tracker import router as smoking_router
from api.workout_tracker import router as workout_router
from api.health import router as health_router
from api.db_tasks import router as db_tasks_router
from api.dashboard import router as dashboard_router

settings = Settings()

# Skip logging setup during testing
if not os.getenv("TESTING"):
    setup_logging(settings)

app = FastAPI(title=settings.app_name)

app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.cors_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(dashboard_router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(smoking_router, prefix="/api/smoking", tags=["smoking"])
app.include_router(workout_router, prefix="/api/workouts", tags=["workouts"])
app.include_router(health_router, prefix="/api/health", tags=["health"])
app.include_router(db_tasks_router, prefix="/db", tags=["database"])


@app.get("/")
def read_root():
	return {"status": "ok", "message": settings.app_name}


@app.on_event("startup")
def on_startup():
	# Skip database initialization during testing
	if not os.getenv("TESTING"):
		logging.getLogger("uvicorn").info("Starting up application")
		# Initialize DB (creates tables for imported models)
		init_db()


@app.on_event("shutdown")
def on_shutdown():
	if not os.getenv("TESTING"):
		logging.getLogger("uvicorn").info("Shutting down application")


if __name__ == "__main__":
	import uvicorn

	uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
