from dataclasses import dataclass


@dataclass
class FloodReport:
    created_at: str
    latitude: float
    longitude: float
    location_name: str
    flood_level: str
    road_condition: str
    needs: str
    notes: str
    verification_status: str = "unverified"
    confirmations: int = 0
    id: int | None = None
