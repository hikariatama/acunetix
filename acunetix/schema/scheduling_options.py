import dataclasses
import datetime
import typing


@dataclasses.dataclass
class SchedulingOptions:
    disable: bool
    time_sensitive: bool
    triggerable: bool
    history_limit: typing.Optional[int] = None
    recurrence: typing.Optional[str] = None
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

        if not data["recurrence"]:
            data.pop("recurrence")

        if not data["history_limit"]:
            data.pop("history_limit")

        return data
