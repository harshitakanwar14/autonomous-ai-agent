
import sqlite3
import json
import uuid

from pathlib import Path
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "agent_memory.db"


class AgentMemory:

    def __init__(self):
        self.initialize_database()

    def connect(self):
        return sqlite3.connect(DATABASE_PATH)

    def initialize_database(self):

        with self.connect() as connection:

            connection.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    goal TEXT NOT NULL,
                    plan TEXT,
                    status TEXT,
                    created_at TEXT
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    iteration INTEGER,
                    observation TEXT,
                    FOREIGN KEY(run_id) REFERENCES runs(run_id)
                )
            """)

    def start_run(self, goal, plan):

        run_id = str(uuid.uuid4())

        with self.connect() as connection:

            connection.execute("""
                INSERT INTO runs
                (run_id, goal, plan, status, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                run_id,
                goal,
                json.dumps(plan, default=str),
                "running",
                datetime.now(timezone.utc).isoformat()
            ))

        return run_id

    def add_observation(
        self,
        run_id,
        iteration,
        observation
    ):

        with self.connect() as connection:

            connection.execute("""
                INSERT INTO observations
                (run_id, iteration, observation)
                VALUES (?, ?, ?)
            """, (
                run_id,
                iteration,
                json.dumps(observation, default=str)
            ))

    def get_history(self, run_id):

        with self.connect() as connection:

            rows = connection.execute("""
                SELECT observation
                FROM observations
                WHERE run_id = ?
                ORDER BY iteration
            """, (run_id,)).fetchall()

        return [
            json.loads(row[0])
            for row in rows
        ]

    def update_status(self, run_id, status):

        with self.connect() as connection:

            connection.execute("""
                UPDATE runs
                SET status = ?
                WHERE run_id = ?
            """, (status, run_id))
