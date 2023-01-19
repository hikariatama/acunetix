import dataclasses
import datetime
import typing

from .notification_data import NotificationData


@dataclasses.dataclass
class Notification:
    consumed: bool
    created: datetime.datetime
    data: NotificationData
    email: typing.Optional[str]
    notification_id: str
    resource_id: str
    resource_type: int
    severity: int
    type_id: int
    user_id: typing.Optional[str]

    @classmethod
    def from_dict(cls, data: dict):
        data["created"] = datetime.datetime.fromisoformat(data["created"])
        data["data"] = NotificationData.from_dict(data["data"])
        return cls(**data)

    def to_json(self):
        data = dataclasses.asdict(self)
        data["created"] = data["created"].isoformat()
        return data
