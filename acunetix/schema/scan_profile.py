import dataclasses
import typing


@dataclasses.dataclass
class ScanProfile:
    profile_id: str
    checks: typing.List[str]
    custom: bool
    name: str
    sort_order: int

    @classmethod
    def from_dict(cls, data: dict) -> "ScanProfile":
        return cls(**data)

    def to_json(self) -> dict:
        return dataclasses.asdict(self)


FULL_SCAN = ScanProfile(
    "11111111-1111-1111-1111-111111111111",
    [],
    False,
    "Full Scan",
    10,
)

HIGH_RISK_VULNERABILITIES = ScanProfile(
    "11111111-1111-1111-1111-111111111112",
    [],
    False,
    "High Risk Vulnerabilities",
    20,
)

HIGH_OR_MEDIUM_RISK_VULNERABILITIES = ScanProfile(
    "11111111-1111-1111-1111-111111111119",
    [],
    False,
    "High or Medium Risk Vulnerabilities",
    30,
)

CROSS_SITE_SCRIPTING_VULNERABILITIES = ScanProfile(
    "11111111-1111-1111-1111-111111111116",
    [],
    False,
    "Cross-site Scripting Vulnerabilities",
    40,
)

SQL_INJECTION_VULNERABILITIES = ScanProfile(
    "11111111-1111-1111-1111-111111111113",
    [],
    False,
    "SQL Injection Vulnerabilities",
    50,
)

WEAK_PASSWORDS = ScanProfile(
    "11111111-1111-1111-1111-111111111115",
    [],
    False,
    "Weak Passwords",
    60,
)

CRAWL_ONLY = ScanProfile(
    "11111111-1111-1111-1111-111111111117",
    [],
    False,
    "Crawl Only",
    70,
)

MALWARE_SCAN = ScanProfile(
    "11111111-1111-1111-1111-111111111120",
    [],
    False,
    "Malware Scan",
    90,
)
