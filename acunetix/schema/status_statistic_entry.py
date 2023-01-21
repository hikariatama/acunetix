import dataclasses


@dataclasses.dataclass
class StatusStatisticEntry:
    number_of_runs: int
    operation_name: str
    total_duration: int
    average_duration: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_json(self):
        return dataclasses.asdict(self)
