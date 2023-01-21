import dataclasses
import typing


@dataclasses.dataclass
class StatusStatisticEntry:
    number_of_runs: typing.Optional[int] = None
    operation_name: typing.Optional[str] = None
    total_duration: typing.Optional[int] = None
    average_duration: typing.Optional[int] = None
    location_name: typing.Optional[str] = None
    number_of_requests: typing.Optional[int] = None
    total_duration: typing.Optional[int] = None
    average_duration: typing.Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_json(self):
        data = dataclasses.asdict(self)
        if data["number_of_runs"] is None:
            data.pop("number_of_runs")
        if data["operation_name"] is None:
            data.pop("operation_name")
        if data["total_duration"] is None:
            data.pop("total_duration")
        if data["average_duration"] is None:
            data.pop("average_duration")
        if data["location_name"] is None:
            data.pop("location_name")
        if data["number_of_requests"] is None:
            data.pop("number_of_requests")
        if data["total_duration"] is None:
            data.pop("total_duration")
        if data["average_duration"] is None:
            data.pop("average_duration")

        return data
