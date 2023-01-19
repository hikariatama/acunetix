import dataclasses
import datetime
import typing


@dataclasses.dataclass
class Target:
    address: str
    criticality: int
    description: str
    type: str
    continuous_mode: typing.Optional[bool] = None
    default_scanning_profile_id: typing.Optional[str] = None
    deleted_at: typing.Optional[datetime.datetime] = None
    fqdn: typing.Optional[str] = None
    fqdn_hash: typing.Optional[str] = None
    fqdn_status: typing.Optional[str] = None
    fqdn_tm_hash: typing.Optional[str] = None
    issue_tracker_id: typing.Optional[str] = None
    last_scan_date: typing.Optional[datetime.datetime] = None
    last_scan_id: typing.Optional[str] = None
    last_scan_session_id: typing.Optional[str] = None
    last_scan_session_status: typing.Optional[str] = None
    manual_intervention: typing.Optional[bool] = None
    severity_counts: typing.Optional[dict] = None
    target_id: typing.Optional[str] = None
    threat: typing.Optional[int] = None
    verification: typing.Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        if data.get("deleted_at"):
            data["deleted_at"] = datetime.datetime.fromisoformat(data["deleted_at"])
        if data.get("last_scan_date"):
            data["last_scan_date"] = datetime.datetime.fromisoformat(
                data["last_scan_date"]
            )
        return cls(**data)

    def to_json(self):
        data = dataclasses.asdict(self)

        if data["deleted_at"]:
            data["deleted_at"] = data["deleted_at"].isoformat()

        if data["last_scan_date"]:
            data["last_scan_date"] = data["last_scan_date"].isoformat()

        return data
