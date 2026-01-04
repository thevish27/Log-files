"""
Log File Analysis API with MySQL
Built using FastAPI
"""

import mysql.connector
import hashlib #unique id generation
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# -------------------------
# CONFIG
# -------------------------
LOG_DIRECTORY = Path(__file__).parent / "logs"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root@123",
    "database": "logdb"
}

# -------------------------
# FASTAPI APP
# -------------------------
app = FastAPI(
    title="Log File Analysis API",
    version="1.0.0"
)

# -------------------------
# MODELS
# -------------------------
class LogEntry(BaseModel):
    id: str
    timestamp: str
    level: str
    component: str
    message: str
    source_file: str

# -------------------------
# DB CONNECTION
# -------------------------
def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# -------------------------
# UTILS
# -------------------------
def generate_log_id(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

# -------------------------
# LOAD LOG FILES → DB
# -------------------------
def insert_logs_into_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id VARCHAR(20) PRIMARY KEY,
            timestamp VARCHAR(30),
            level VARCHAR(10),
            component VARCHAR(50),
            message TEXT,
            source_file VARCHAR(50)
        )
    """)

    insert_sql = """
        INSERT IGNORE INTO logs
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    for file in LOG_DIRECTORY.glob("*.log"):
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("Timestamp"):
                    continue

                parts = line.split("\t")
                if len(parts) < 4:
                    continue

                log_id = generate_log_id(line + file.name)

                cur.execute(insert_sql, (
                    log_id,
                    parts[0],
                    parts[1],
                    parts[2],
                    parts[3],
                    file.name
                ))

    conn.commit()
    cur.close()
    logger.info("Data inserted succesfully")
    conn.close()

# -------------------------
# RUN ON STARTUP
# -------------------------
@app.on_event("startup")
def startup():
    insert_logs_into_db()

# -------------------------
# API ENDPOINTS
# -------------------------

@app.get("/")
def home():
    return {"message": "Log API running"}

# ✅ GET LOGS (Pagination + Filter)
@app.get("/logs")
def get_logs(
    level: Optional[str] = None,
    page: int = 1,
    page_size: int = 10
):
    offset = (page - 1) * page_size
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    query = "SELECT * FROM logs"
    params = []

    if level:
        query += " WHERE level = %s"
        params.append(level)

    query += " LIMIT %s OFFSET %s"
    params.extend([page_size, offset])

    cur.execute(query, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()
    logger.info("Data fetched succesfully")

    return rows

# ✅ GET SINGLE LOG
@app.get("/logs/{log_id}")
def get_log(log_id: str):
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM logs WHERE id = %s", (log_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Log not found")

    return row

# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
