import dataclasses
import typing


@dataclasses.dataclass
class InputTarget:
    address: str
    description: typing.Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_json(self):
        data = dataclasses.asdict(self)

        if data["description"] is None:
            data.pop("description")

        return data
