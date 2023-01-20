import dataclasses

from .access_map import AccessMap


@dataclasses.dataclass
class User:
    email: str
    first_name: str
    last_name: str
    role: str
    access: AccessMap
    enabled: bool
    locked: bool
    password: str
    totp_enabled: bool
    user_id: str

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        data["access"] = AccessMap.from_dict(data["access"])
        return cls(**data)

    def to_json(self) -> dict:
        return dataclasses.asdict(self)
