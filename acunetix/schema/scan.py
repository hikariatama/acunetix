import dataclasses
import typing

from .current_session import CurrentSession
from .scheduling_options import SchedulingOptions
from .target import Target


@dataclasses.dataclass
class Scan:
    criticality: int
    current_session: CurrentSession
    incremental: bool
    max_scan_time: int
    profile_id: str
    profile_name: str
    scan_id: str
    schedule: SchedulingOptions
    target: Target
    target_id: str
    report_template_id: typing.Optional[str] = None
    next_run: typing.Optional[int] = None
    manual_intervention: typing.Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict):
        data["current_session"] = CurrentSession.from_dict(data["current_session"])
        data["schedule"] = SchedulingOptions.from_dict(data["schedule"])
        data["target"] = Target.from_dict(data["target"])
        return cls(**data)

    def to_json(self):
        return dataclasses.asdict(self)
