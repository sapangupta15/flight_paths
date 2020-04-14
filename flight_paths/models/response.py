from dataclasses_json import dataclass_json
from dataclasses import dataclass
from typing import Optional, List


@dataclass_json
@dataclass
class Route:
    source_airport: str
    destination_airport: str
    airline: str
    distance: str
    est_travel_time: str
    path: List[List[float]]
    flight_number: str = None


@dataclass_json
@dataclass
class Response:
    source: str
    destination: str
    routes: Optional[List[List[Route]]]
