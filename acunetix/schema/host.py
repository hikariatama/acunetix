import dataclasses
import typing

from .target_host_info import TargetHostInfo
from .web_scan_status import WebScanStatus


@dataclasses.dataclass
class Host:
    host: str
    target_info: TargetHostInfo
    external_hosts: typing.List[str]
    web_scan_status: WebScanStatus
    is_starting_host: bool
    aborted_reason: typing.Optional[str] = None
    aborted: typing.Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict):
        if data.get("target_info"):
            data["target_info"] = TargetHostInfo.from_dict(data["target_info"])
        if data.get("web_scan_status"):
            data["web_scan_status"] = WebScanStatus.from_dict(data["web_scan_status"])

        return cls(**data)

    def to_json(self):
        return dataclasses.asdict(self)
