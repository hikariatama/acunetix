import dataclasses


@dataclasses.dataclass
class FileAttachment:
    name: str
    path: str
    type: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_json(self):
        return dataclasses.asdict(self)
