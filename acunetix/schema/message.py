import dataclasses

from .target_info import TargetInfo


@dataclasses.dataclass
class Message:
    data: str
    kind: str
    time: str
    level: int
    target_info: TargetInfo

    @classmethod
    def from_dict(cls, data: dict):
        if data.get("target_info"):
            data["target_info"] = TargetInfo.from_dict(data["target_info"])

        return cls(**data)

    def to_json(self):
        return dataclasses.asdict(self)
