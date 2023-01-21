import dataclasses


@dataclasses.dataclass
class TargetInfo:
    host: str
    target_id: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_json(self):
        return dataclasses.asdict(self)
