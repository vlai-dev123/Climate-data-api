# Climate Data API

A Python project for validating, processing, and analyzing climate emissions data, with both CLI and REST API interfaces.

## Features

- **Data Validation:** Cleans and checks emissions CSV data for errors and warnings.
- **Metric Calculation:** Computes total emissions, carbon intensity, and trends.
- **Facility Aggregation:** Summarizes emissions by facility.
- **REST API:** Upload and process data via FastAPI endpoints.
- **Testing:** Built-in test functions for core logic.

## Project Structure

- `main.py` — CLI demo: validates, processes, aggregates, and tests sample data.
- `climate_io.py` — Core logic for validation and metric calculations.
- `api.py` — FastAPI app for uploading and querying emissions data.
- `testing.py` — Test functions for validation and calculation logic.

## Usage

### CLI Demo

```sh
python main.py
```

### API Server

```sh
uvicorn api:app --reload
```
- Upload endpoint: `POST /api/v1/emissions/upload` (CSV file)
- Facility query: `GET /api/v1/facilities/{facility_id}/emissions`

## Conventions

- All core logic is in `climate_io.py`.
- Data is handled as CSV strings or pandas DataFrames.
- Errors and warnings are returned as lists of strings.
- Tests are simple functions, not using a test framework by default.

## Requirements

- Python 3.8+
- `pandas`
- `fastapi`
- `uvicorn`
- `pydantic`

Install dependencies:
```sh
pip install -r requirements.txt
```

---

**For details on extending or contributing, see `.github/copilot-instructions.md`.**