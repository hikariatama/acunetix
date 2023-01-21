import dataclasses
import typing

from .status_statistic_entry import StatusStatisticEntry


@dataclasses.dataclass
class StatusStatistics:
    operationStatsByRun: typing.List[StatusStatisticEntry]
    locationStatsByRequest: typing.List[StatusStatisticEntry]
    locationStatsByAvgDuration: typing.List[StatusStatisticEntry]
    locationStatsByTotalDuration: typing.List[StatusStatisticEntry]
    operationStatsByTotalDuration: typing.List[StatusStatisticEntry]

    @classmethod
    def from_dict(cls, data: dict):
        data["operationStatsByRun"] = [
            StatusStatisticEntry.from_dict(x) for x in data["operationStatsByRun"]
        ]
        data["locationStatsByRequest"] = [
            StatusStatisticEntry.from_dict(x) for x in data["locationStatsByRequest"]
        ]
        data["locationStatsByAvgDuration"] = [
            StatusStatisticEntry.from_dict(x)
            for x in data["locationStatsByAvgDuration"]
        ]
        data["locationStatsByTotalDuration"] = [
            StatusStatisticEntry.from_dict(x)
            for x in data["locationStatsByTotalDuration"]
        ]
        data["operationStatsByTotalDuration"] = [
            StatusStatisticEntry.from_dict(x)
            for x in data["operationStatsByTotalDuration"]
        ]

        return cls(**data)

    def to_json(self):
        return dataclasses.asdict(self)
