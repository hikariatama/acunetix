import dataclasses


@dataclasses.dataclass
class WebScanStatus:
    locations: int
    request_count: int
    avg_response_time: int
    max_response_time: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_json(self):
        return dataclasses.asdict(self)
