import typing

from ..schema import Scan, SchedulingOptions, WebVulnerabilityScanner
from ..typehints import (
    CallbackFunction,
    InputReportTemplate,
    InputScan,
    InputScanProfile,
    InputTargetType,
)
from ..utils import (
    get_input_report_template_id,
    get_input_scan_id,
    get_input_scan_profile_id,
    get_input_target_id,
)


class Scans:
    """Scans methods"""

    async def get_scans(self) -> typing.List[Scan]:
        """
        Get all scans
        :return: List of `Scan` objects
        :example:
        ```python
            >>> scans = await api.scans.get_scans()
            >>> for scan in scans:
            >>>     print(scan)
        ```
        """
        return [
            Scan.from_dict(scan)
            for scan in (await self.request("GET", "scans"))["scans"]
        ]

    async def get_scan(self, scan: InputScan) -> Scan:
        """
        Get scan by ID
        :param scan: Scan ID or `Scan` object
        :return: `Scan` object
        :example:
        ```python
            >>> scan = await api.scans.get_scan(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> print(scan)
            >>> scan = await api.scans.get_scan(
                    Scan(...),
                )
            >>> print(scan)
        ```
        """
        return Scan.from_dict(
            await self.request("GET", f"scans/{get_input_scan_id(scan)}")
        )

    async def create_scan(
        self,
        target: InputTargetType,
        profile: InputScanProfile,
        report_template: typing.Optional[InputReportTemplate] = None,
        schedule: typing.Optional[SchedulingOptions] = None,
        done_callback: typing.Optional[CallbackFunction] = None,
    ) -> Scan:
        """
        Create new scan
        :param target: Target ID or `Target` object
        :param profile: Profile ID or `ScanProfile` object
        :param report_template: Report template ID or `ReportTemplate` object
        :param schedule: Scheduling options
        :param done_callback: Callback function that will be called
                              when scan is finished (not report ready!)
        :return: `Scan` object
        :example:
        ```python
            >>> scan = await api.scans.create_scan(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                    "11111111-1111-1111-1111-111111111111",
                )
            >>> print(scan)
        ```
        """

        if not schedule:
            schedule = SchedulingOptions(
                disable=False,
                history_limit=0,
                recurrence=0,
                start_date=None,
                time_sensitive=False,
                triggerable=False,
            )

        response: dict = await self.request(
            "POST",
            "scans",
            {
                "profile_id": get_input_scan_profile_id(profile),
                "target_id": get_input_target_id(target),
                "schedule": schedule,
                **(
                    {
                        "report_template_id": get_input_report_template_id(
                            report_template
                        )
                    }
                    if report_template
                    else {}
                ),
            },
        )

        if "scan_id" not in response:
            raise ValueError("Invalid response")

        if done_callback:
            self._callbacks[response["scan_id"]] = done_callback

        return await self.get_scan(response["scan_id"])

    async def delete_scan(self, scan: InputScan) -> None:
        """
        Delete scan by ID
        :param scan: Scan ID or `Scan` object
        :example:
        ```python
            >>> await api.scans.delete_scan(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> await api.scans.delete_scan(Scan(...))
        ```
        """
        await self.request("DELETE", f"scans/{get_input_scan_id(scan)}")

    async def pause_scan(self, scan: InputScan) -> None:
        """
        Pause scan by ID
        :param scan: Scan ID or `Scan` object
        :example:
        ```python
            >>> await api.scans.pause_scan(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> await api.scans.pause_scan(Scan(...))
        ```
        """
        await self.request("POST", f"scans/{get_input_scan_id(scan)}/pause", {})

    async def resume_scan(self, scan: InputScan) -> None:
        """
        Resume scan by ID
        :param scan: Scan ID or `Scan` object
        :example:
        ```python
            >>> await api.scans.resume_scan(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> await api.scans.resume_scan(Scan(...))
        ```
        """
        await self.request("POST", f"scans/{get_input_scan_id(scan)}/resume", {})

    async def stop_scan(self, scan: InputScan) -> None:
        """
        Stop scan by ID
        :param scan: Scan ID or `Scan` object
        :example:
        ```python
            >>> await api.scans.stop_scan(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> await api.scans.stop_scan(Scan(...))
        ```
        """
        await self.request("POST", f"scans/{get_input_scan_id(scan)}/abort", {})

    async def get_current_stats(self, scan: InputScan) -> WebVulnerabilityScanner:
        """
        Get current stats of scan
        :param scan: Scan ID or `Scan` object
        :return: `WebVulnerabilityScanner` object
        :example:
        ```python
            >>> stats = await api.scans.get_current_stats(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> print(stats)
            >>> stats = await api.scans.get_current_stats(Scan(...))
            >>> print(stats)
        ```
        """
        scan = await self.get_scan(scan)
        return WebVulnerabilityScanner.from_dict(
            (
                await self.request(
                    "GET",
                    f"scans/{get_input_scan_id(scan)}/results/{scan.current_session.scan_session_id}/statistics",
                )
            )["scanning_app"]["wvs"]
        )
