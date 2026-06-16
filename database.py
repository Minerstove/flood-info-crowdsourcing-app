import sqlite3
from pathlib import Path

from models import FloodReport


DATA_DIR = Path(__file__).resolve().parent / "data"
DB_PATH = DATA_DIR / "flood_reports.db"


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_table() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS flood_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                location_name TEXT,
                flood_level TEXT NOT NULL,
                road_condition TEXT NOT NULL,
                needs TEXT,
                notes TEXT,
                verification_status TEXT DEFAULT 'unverified',
                confirmations INTEGER DEFAULT 0
            )
            """
        )


def add_report(report: FloodReport) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO flood_reports (
                created_at,
                latitude,
                longitude,
                location_name,
                flood_level,
                road_condition,
                needs,
                notes,
                verification_status,
                confirmations
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                report.created_at,
                report.latitude,
                report.longitude,
                report.location_name,
                report.flood_level,
                report.road_condition,
                report.needs,
                report.notes,
                report.verification_status,
                report.confirmations,
            ),
        )
        return int(cursor.lastrowid)


def get_reports() -> list[FloodReport]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                id,
                created_at,
                latitude,
                longitude,
                location_name,
                flood_level,
                road_condition,
                needs,
                notes,
                verification_status,
                confirmations
            FROM flood_reports
            ORDER BY created_at DESC
            """
        ).fetchall()

    return [FloodReport(**dict(row)) for row in rows]


def verify_report(report_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE flood_reports SET verification_status = ? WHERE id = ?",
            ("verified", report_id),
        )


def resolve_report(report_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE flood_reports SET verification_status = ? WHERE id = ?",
            ("resolved", report_id),
        )
