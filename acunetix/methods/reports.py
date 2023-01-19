import typing

from ..schema import Report, TypedList


class Reports:
    async def get_reports(self) -> typing.List[Report]:
        """
        Get all reports
        :return: List of `Report` objects
        :example:
        ```python
            >>> reports = await api.reports.get_reports()
            >>> for report in reports:
            >>>     print(report)
        ```
        """
        return [
            Report.from_dict(report)
            for report in (await self._request("GET", "reports"))["reports"]
        ]

    async def get_report(self, report_id: str) -> Report:
        """
        Get report by ID
        :param report_id: Report ID
        :return: `Report` object
        :example:
        ```python
            >>> report = await api.reports.get_report(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> print(report)
        ```
        """
        return Report.from_dict(await self._request("GET", f"reports/{report_id}"))

    async def create_report(
        self,
        template_id: str,
        source: TypedList,
    ) -> Report:
        """
        Create new report
        :param template_id: Report template ID
        :param source: `TypedList` object
        :return: `Report` object
        :example:
        ```python
            >>> report = await api.reports.create_report(
                    "11111111-1111-1111-1111-111111111111",
                    TypedList(
                        "scans",
                        [
                            "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                            "316f58ff-f6d6-47d5-b5e3-806837a8cfe3",
                        ],
                    ),
                )
            >>> print(report)
        ```
        """
        data = {"template_id": template_id, "source": source}
        response = await self._request("POST", "reports", data)

        if "report_id" not in response:
            raise ValueError("Invalid response")

        return await self.get_report(response["report_id"])
