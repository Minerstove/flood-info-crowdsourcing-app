from datetime import datetime

import pandas as pd

import database
from models import FloodReport


MARKER_COLORS = {
    "ankle_deep": "green",
    "knee_deep": "orange",
    "waist_deep": "red",
    "chest_deep": "darkred",
    "not_passable": "black",
}


def submit_flood_report(report_data: dict) -> int:
    latitude = report_data.get("latitude")
    longitude = report_data.get("longitude")
    flood_level = report_data.get("flood_level")
    road_condition = report_data.get("road_condition")

    if latitude is None or longitude is None:
        raise ValueError("Latitude and longitude are required.")
    if not flood_level:
        raise ValueError("Flood level is required.")
    if not road_condition:
        raise ValueError("Road condition is required.")

    if flood_level == "not_passable":
        road_condition = "blocked"

    report = FloodReport(
        created_at=datetime.now().isoformat(timespec="seconds"),
        latitude=float(latitude),
        longitude=float(longitude),
        location_name=report_data.get("location_name", "").strip(),
        flood_level=flood_level,
        road_condition=road_condition,
        needs=", ".join(report_data.get("needs", [])),
        notes=report_data.get("notes", "").strip(),
    )
    return database.add_report(report)


def get_marker_color(flood_level: str) -> str:
    return MARKER_COLORS.get(flood_level, "blue")


def reports_to_dataframe(reports: list[FloodReport]) -> pd.DataFrame:
    rows = []
    for report in reports:
        row = report.__dict__.copy()
        row["age_hours"] = get_report_age_hours(report.created_at)
        row["status_age_label"] = get_age_label(row["age_hours"])
        rows.append(row)

    return pd.DataFrame(rows)


def get_report_age_hours(created_at: str) -> float:
    created = datetime.fromisoformat(created_at)
    age = datetime.now() - created
    return round(age.total_seconds() / 3600, 2)


def get_age_label(age_hours: float) -> str:
    if age_hours > 12:
        return "expired"
    if age_hours > 6:
        return "possibly outdated"
    return "active"
