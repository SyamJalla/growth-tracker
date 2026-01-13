# Testing Guide

## Current Test Coverage

### Test Files Created
- `conftest.py` - Test fixtures and configuration
- `test_app.py` - Root and health endpoint tests
- `test_dashboard.py` - Dashboard endpoint tests (9 tests)
- `test_workout_tracker.py` - Workout CRUD tests (18 tests)
- `test_smoking_tracker.py` - Smoking CRUD tests (18 tests)
- `test_kpi_calculations.py` - KPI calculation logic tests (13 tests)
- `test_models_db.py` - Database model tests (20 tests)

### Total Tests: 80+ comprehensive tests

## Running Tests

```bash
cd Backend
python -m pytest -v
```

### Run with coverage report:
```bash
python -m pytest -v --cov=. --cov-report=html
```

### Run specific test file:
```bash
python -m pytest tests/test_dashboard.py -v
```

### Run specific test:
```bash
python -m pytest tests/test_dashboard.py::test_dashboard_empty -v
```

## Known Issues to Fix

### 1. Database Connection Issue
Tests are currently trying to connect to PostgreSQL instead of using the in-memory SQLite database. This happens because the FastAPI app startup event runs `init_db()` before the test fixture can override the database dependency.

**Solution**: Need to modify the app to skip database initialization during testing, or refactor to use lifespan events properly.

### 2. Enum Value Mismatches
Some test files use incorrect enum values (e.g., `WorkoutType.GYM` instead of `WorkoutType.PUSH`).

**Correct Enum Values**:
- WorkoutType: PUSH, PULL, LEGS, UPPER, LOWER, CARDIO, OTHERS
- IntensityLevel: LOW, MODERATE, HIGH
- SmokingLocation: HOME, WORK, SOCIAL, OTHER

## Test Structure

### Fixtures (conftest.py)
- `db_session`: Fresh in-memory SQLite database for each test
- `client`: FastAPI TestClient with database override
- `sample_workout_data`: Sample workout entry data
- `sample_smoking_data`: Sample smoking entry data
- `multiple_workout_entries`: 4 workout entries for testing streaks
- `multiple_smoking_entries`: 4 smoking entries for testing statistics

### Test Categories

#### API Endpoint Tests
- CREATE operations (POST)
- READ operations (GET single, GET list)
- UPDATE operations (PUT)
- DELETE operations
- Query parameters (date ranges, limits)
- Error cases (404, 400, 422)

#### Business Logic Tests
- Streak calculations (workout streaks, smoke-free streaks)
- Statistical aggregations (averages, totals, percentages)
- Edge cases (empty data, all zeros, etc.)

#### Database Model Tests
- Model creation and validation
- Primary key constraints
- Enum validations
- Optional field handling
- CRUD operations at DB level

## Configuration Files

### pytest.ini
- Test discovery patterns
- Output verbosity
- Coverage configuration
- Custom markers for test organization

### .coveragerc
- Coverage source directories
- Files/directories to omit
- Report formatting options
- Minimum coverage thresholds

## Next Steps

1. Fix database connection issue in tests
2. Update enum values in test files
3. Run full test suite
4. Generate coverage report
5. Add integration tests for multi-endpoint workflows
6. Set up CI/CD pipeline for automated testing
