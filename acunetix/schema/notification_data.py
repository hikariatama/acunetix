import dataclasses
import datetime
import typing

from .file_attachment import FileAttachment


@dataclasses.dataclass
class NotificationData:
    ended: typing.Optional[datetime.datetime] = None
    started: typing.Optional[datetime.datetime] = None
    name: typing.Optional[str] = None
    source: typing.Optional[str] = None
    creator: typing.Optional[str] = None
    source_type: typing.Optional[str] = None
    template_name: typing.Optional[str] = None
    target_id: typing.Optional[str] = None
    vuln_stats: typing.Optional[typing.List[int]] = None
    event_level: typing.Optional[int] = None
    target_desc: typing.Optional[typing.List[str]] = None
    profile_name: typing.Optional[str] = None
    scan_session_id: typing.Optional[str] = None
    failed_job_count: typing.Optional[int] = None
    file_attachments: typing.Optional[typing.List[typing.Dict[str, str]]] = None

    @classmethod
    def from_dict(cls, data: dict):
        if data.get("file_attachments"):
            data["file_attachments"] = [
                FileAttachment.from_dict(x) for x in data["file_attachments"]
            ]
        return cls(**data)

    def to_json(self):
        return dataclasses.asdict(self)
