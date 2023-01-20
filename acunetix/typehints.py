import typing

from .schema import Report, ReportTemplate, Scan, ScanProfile, Target, User

InputReport = typing.Union[Report, str]
InputScan = typing.Union[Scan, str]
InputTargetType = typing.Union[Target, str]
InputReportTemplate = typing.Union[ReportTemplate, str]
InputUser = typing.Union[User, str]
InputScanProfile = typing.Union[ScanProfile, str]
CallbackFunction = typing.Union[typing.Callable, typing.Callable[..., typing.Awaitable]]
