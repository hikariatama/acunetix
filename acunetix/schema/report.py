import dataclasses
import datetime
import typing

from .report_template import TEMPLATE_MAP, ReportTemplate
from .typed_list import TypedList


@dataclasses.dataclass
class Report:
    download: typing.List[str]
    generation_date: datetime.datetime
    report_id: str
    status: str
    source: TypedList
    template: typing.Optional[ReportTemplate] = None
    template_id: typing.Optional[str] = None
    template_name: typing.Optional[str] = None
    template_type: typing.Optional[int] = None

    def __post_init__(self):
        if self.template:
            if self.template_id is None:
                self.template_id = self.template.template_id

            if self.template_name is None:
                self.template_name = self.template.name

            if self.template_type is None:
                self.template_type = 0

    @classmethod
    def from_dict(cls, data: dict):
        data["generation_date"] = datetime.datetime.fromisoformat(
            data["generation_date"]
        )
        data["source"] = TypedList.from_dict(data["source"])
        data.setdefault(
            "template",
            TEMPLATE_MAP.get(data.get("template_id"), None),
        )

        return cls(**data)

    def to_json(self):
        data = dataclasses.asdict(self)
        data["generation_date"] = data["generation_date"].isoformat()
        data.pop("template", None)
        return data
