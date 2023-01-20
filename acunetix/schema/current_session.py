import dataclasses
import datetime
import typing


@dataclasses.dataclass
class CurrentSession:
    event_level: int
    progress: int
    scan_session_id: str
    severity_counts: dict
    status: str
    threat: int
    start_date: typing.Optional[datetime.datetime] = None

    @classmethod
    def from_dict(cls, data: dict):
        if data.get("start_date"):
            data["start_date"] = datetime.datetime.fromisoformat(data["start_date"])

        return cls(**data)

    def to_json(self):
        data = dataclasses.asdict(self)

        if data["start_date"]:
            data["start_date"] = data["start_date"].isoformat()

        return data
