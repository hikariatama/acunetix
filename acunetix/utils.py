import asyncio
import functools
import typing

from .schema import Report, ReportTemplate, Scan, ScanProfile, Target, User


def get_input_user_id(user: typing.Union[User, str]) -> str:
    """
    Get user ID from `User` object or string
    :param user: `User` object or string with user ID
    :return: User ID
    :example:
    ```python
        >>> user_id = get_input_user_id(
                "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
            )
        >>> print(user_id)
        >>> user_id = get_input_user_id(User(...))
        >>> print(user_id)
    ```
    """
    return user.user_id if isinstance(user, User) else user


def get_input_target_id(target: typing.Union[Target, str]) -> str:
    """
    Get target ID from `Target` object or string
    :param target: `Target` object or string with target ID
    :return: Target ID
    :example:
    ```python
        >>> target_id = get_input_target_id(
                "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
            )
        >>> print(target_id)
        >>> target_id = get_input_target_id(Target(...))
        >>> print(target_id)
    ```
    """
    return target.target_id if isinstance(target, Target) else target


def get_input_scan_id(scan: typing.Union[Scan, str]) -> str:
    """
    Get scan ID from `Scan` object or string
    :param scan: `Scan` object or string with scan ID
    :return: Scan ID
    :example:
    ```python
        >>> scan_id = get_input_scan_id(
                "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
            )
        >>> print(scan_id)
        >>> scan_id = get_input_scan_id(Scan(...))
        >>> print(scan_id)
    ```
    """
    return scan.scan_id if isinstance(scan, Scan) else scan


def get_input_report_template_id(
    report_template: typing.Union[ReportTemplate, str]
) -> str:
    """
    Get report template ID from `ReportTemplate` object or string
    :param report_template: `ReportTemplate` object or string with report template ID
    :return: Report template ID
    :example:
    ```python
        >>> report_template_id = get_input_report_template_id(
                "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
            )
        >>> print(report_template_id)
        >>> report_template_id = get_input_report_template_id(ReportTemplate(...))
        >>> print(report_template_id)
    ```
    """
    return (
        report_template.template_id
        if isinstance(report_template, ReportTemplate)
        else report_template
    )


def get_input_report_id(report: typing.Union[Report, str]) -> str:
    """
    Get report ID from `Report` object or string
    :param report: `Report` object or string with report ID
    :return: Report ID
    :example:
    ```python
        >>> report_id = get_input_report_id(
                "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
            )
        >>> print(report_id)
        >>> report_id = get_input_report_id(Report(...))
        >>> print(report_id)
    ```
    """
    return report.report_id if isinstance(report, Report) else report


def get_input_scan_profile_id(scan_profile: typing.Union[ScanProfile, str]) -> str:
    """
    Get scan profile ID from `ScanProfile` object or string
    :param scan_profile: `ScanProfile` object or string with scan profile ID
    :return: Scan profile ID
    :example:
    ```python
        >>> scan_profile_id = get_input_scan_profile_id(
                "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
            )
        >>> print(scan_profile_id)
        >>> scan_profile_id = get_input_scan_profile_id(ScanProfile(...))
        >>> print(scan_profile_id)
    ```
    """
    return (
        scan_profile.profile_id
        if isinstance(scan_profile, ScanProfile)
        else scan_profile
    )


# https://github.com/hikariatama/Hikka/blob/fd918af4f4a9a91dac04f05ad643956b9b709059/hikka/utils.py#L310
def run_sync(func, *args, **kwargs) -> asyncio.Future:
    """
    Run a non-async function in a new thread and return an awaitable
    :param func: Sync-only function to execute
    :return: Awaitable coroutine
    """
    return asyncio.get_event_loop().run_in_executor(
        None,
        functools.partial(func, *args, **kwargs),
    )
