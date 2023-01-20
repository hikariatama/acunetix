import dataclasses
import typing


@dataclasses.dataclass
class AccessMap:
    access_all_groups: bool
    group_id_list: typing.List[str]

    @classmethod
    def from_dict(cls, data: dict) -> "AccessMap":
        return cls(**data)

    def to_json(self) -> dict:
        return dataclasses.asdict(self)
