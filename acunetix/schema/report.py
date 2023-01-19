import dataclasses
import datetime
import typing

from .typed_list import TypedList


@dataclasses.dataclass
class Report:
    download: typing.List[str]
    generation_date: datetime.datetime
    report_id: str
    status: str
    template_id: str
    template_name: str
    template_type: int
    source: TypedList

    @classmethod
    def from_dict(cls, data: dict):
        data["generation_date"] = datetime.datetime.fromisoformat(
            data["generation_date"]
        )
        data["source"] = TypedList.from_dict(data["source"])
        return cls(**data)

    def to_json(self):
        data = dataclasses.asdict(self)
        data["generation_date"] = data["generation_date"].isoformat()
        return data
