import dataclasses
import datetime


@dataclasses.dataclass
class CurrentSession:
    event_level: int
    progress: int
    scan_session_id: str
    severity_counts: dict
    start_date: datetime.datetime
    status: str
    threat: int

    @classmethod
    def from_dict(cls, data: dict):
        data["start_date"] = datetime.datetime.fromisoformat(data["start_date"])
        return cls(**data)

    def to_json(self):
        data = dataclasses.asdict(self)
        data["start_date"] = data["start_date"].isoformat()
        return data
