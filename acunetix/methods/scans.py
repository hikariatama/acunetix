import typing

from ..schema import Scan, SchedulingOptions


class Scans:
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
            for scan in (await self._request("GET", "scans"))["scans"]
        ]

    async def get_scan(self, scan_id: str) -> Scan:
        """
        Get scan by ID
        :param scan_id: Scan ID
        :return: `Scan` object
        :example:
        ```python
            >>> scan = await api.scans.get_scan(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> print(scan)
        ```
        """
        return Scan.from_dict(await self._request("GET", f"scans/{scan_id}"))

    async def create_scan(
        self,
        target_id: str,
        profile_id: str,
        report_template_id: typing.Optional[str] = None,
        schedule: typing.Optional[SchedulingOptions] = None,
        done_callback: typing.Optional[
            typing.Union[typing.Callable, typing.Callable[..., typing.Awaitable]]
        ] = None,
    ) -> Scan:
        """
        Create new scan
        :param target_id: Target ID
        :param profile_id: Profile ID
        :param report_template_id: Report template ID
        :param schedule: Scheduling options
        :param done_callback: Callback function that will be called
                              when scan is finished (not report ready!)
        :return: `Scan` object
        :example:
        ```python
            >>> scan = await api.scans.create_scan(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                    "11111111-1111-1111-1111-111111111111"б
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

        data = {
            "profile_id": profile_id,
            "target_id": target_id,
            "schedule": schedule,
            **(
                {"report_template_id": report_template_id} if report_template_id else {}
            ),
        }
        response = await self._request("POST", "scans", data)

        if "scan_id" not in response:
            raise ValueError("Invalid response")

        if done_callback:
            self._callbacks[response["scan_id"]] = done_callback

        return await self.get_scan(response["scan_id"])
