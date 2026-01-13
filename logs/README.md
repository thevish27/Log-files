# Log File Analysis REST API

A FastAPI-based REST API for accessing and analyzing log file data.

## Features

- **Read and parse log files** from a configured directory
- **Filter logs** by level, component, and time range
- **Get statistics**Understood.
Below is **ONE SINGLE README.md FILE ONLY** — clean, correct, and matching your current project.

👉 **Copy everything below and save it as `README.md`**
(No extra explanations, no multiple versions.)

---

```md
# Log File Analysis REST API (FastAPI + MySQL)

A REST API built using FastAPI that reads log files from a folder, stores them in a MySQL database, and provides endpoints to retrieve and filter log data.

---

## Features
- Read and parse `.log` files
- Store logs in MySQL database
- Generate unique ID for each log entry
- Fetch logs with pagination
- Filter logs by log level
- Retrieve single log by ID

---

## Technologies
- Python
- FastAPI
- MySQL
- Uvicorn

---

## Project Structure
```

Logs-files/
├── app.py
├── logs/
│   └── app.log
├── venv/
└── README.md

```

---

## Log File Format
Log entries must be TAB separated:

```

Timestamp	Level	Component	Message

```

Example:
```

2024-01-01 10:00:00	INFO	AUTH	User logged in

````

---

## Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
````

2. Install dependencies:

```bash
pip install fastapi uvicorn mysql-connector-python
```

3. Create MySQL database:

```sql
CREATE DATABASE logdb;
```

---

## Running the API

Start the server:

```bash
uvicorn main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

---

## API Endpoints

* `GET /` → API status
* `GET /logs` → Get all logs
* `GET /logs?level=ERROR&page=1&page_size=10` → Filter logs
* `GET /logs/{log_id}` → Get single log

---

## Application Flow

* On startup, the application reads all `.log` files from the `logs/` folder
* Log entries are parsed and stored in MySQL
* Duplicate logs are ignored
* APIs fetch data from the database

---

## Short Interview Explanation

This project demonstrates backend development using FastAPI.
It covers file handling, database integration, and REST API development with filtering and pagination.

---

## Author

Vaishnavi Kanawade

```

---

✅ **This is ONE single README.md file.**  
If you want it **even shorter**, just say **“short”**.
```
 on log entries
- **Pagination support** for handling large datasets
- **Unique log IDs** for referencing specific entries

## Installation

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  #  Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirement.txt
```

## Running the API

Start the server:

```bash
uvicorn main:app --reload --port 8000
```
http://localhost:8000
The API will be available at ``

## API Documentation

FastAPI automatically generates interactive documentation:

- **Swagger UI**: h/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### `GET /logs`

Retrieve all log entries with optional filtering and pagination.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | string | Filter by log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `component` | string | Filter by component name |
| `start_time` | string | Filter logs after this timestamp |
| `end_time` | string | Filter logs before this timestamp |
| `page` | int | Page number (default: 1) |
| `page_size` | int | Entries per page (default: 100, max: 1000) |

**Examples:**

```bash
# Get all logs
curl http://localhost:8000/logs

# Filter by level
curl "http://localhost:8000/logs?level=ERROR"

# Filter by component
curl "http://localhost:8000/logs?component=UserAuth"

# Filter by time range
curl "http://localhost:8000/logs?start_time=2025-05-07%2010:00:10&end_time=2025-05-07%2010:00:30"

# Combine filters
curl "http://localhost:8000/logs?level=INFO&component=UserAuth"

# With pagination
curl "http://localhost:8000/logs?page=1&page_size=10"
```

### `GET /logs/stats`

Get aggregate statistics about all log entries.

**Response includes:**
- Total number of log entries
- Counts of log entries per level
- Counts of log entries per component

**Example:**

```bash
curl http://localhost:8000/logs/stats
```

**Sample Response:**

```json
{
  "total_entries": 23,
  "by_level": {
    "INFO": 10,
    "WARNING": 5,http://localhost:8000
    "ERROR": 4,
    "DEBUG": 4
  },
  "by_component": {
    "UserAuth": 5,
    "Payment": 3,
    "Database": 3,
    ...
  }
}
```

### `GET /logs/{log_id}`

Retrieve a specific log entry by its unique ID.

**Example:**

```bash
curl http://localhost:8000/logs/abc123def456
```

**Response:**

```json
{
  "id": "abc123def456",
  "timestamp": "2025-05-07 10:00:20",
  "level": "ERROR",
  "component": "Payment",
  "message": "Transaction failed for user 'jane.doe'.",
  "source_file": "app.log"
}
```

## Log File Format

Log files should be placed in the `logs/` directory with `.log` extension.

Expected format (tab-separated):

```
Timestamp	Level	Component	Message
2025-05-07 10:00:00	INFO	UserAuth	User 'john.doe' logged in successfully.
2025-05-07 10:00:15	WARNING	GeoIP	Could not resolve IP address '192.168.1.100'.
```

## Error Handling

The API returns appropriate HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found (log ID doesn't exist) |
| 500 | Internal Server Error |

## Project Structure

```
log-files/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── logs/               # Log files directory
    ├── app.log
    └── system.log
```