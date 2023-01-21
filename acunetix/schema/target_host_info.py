import dataclasses


@dataclasses.dataclass
class TargetHostInfo:
    os: str
    server: str
    responsive: bool

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_json(self):
        return dataclasses.asdict(self)
