import io
import os
import tempfile
import typing
from urllib import request

from aiofiles import open as aopen
import requests

from ..errors import Acunetix404Error
from ..schema import Report, ReportTemplate, Scan, Target, TypedList
from ..typehints import (
    CallbackFunction,
    InputReport,
    InputReportTemplate,
    InputScan,
    InputTargetType,
)
from ..utils import (
    get_input_report_id,
    get_input_report_template_id,
    get_input_target_id,
    run_sync,
)


class Reports:
    """Reports methods"""

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
            for report in (await self.request("GET", "reports"))["reports"]
        ]

    async def get_report(
        self,
        report: typing.Union[InputReport, InputScan, InputTargetType],
        input_type: typing.Optional[str] = None,
    ) -> Report:
        """
        Get report by ID
        :param report: Report ID, Scan ID, Target ID,
                       `Report`, `Scan` or `Target` object
        :param input_type: Type of input. Can be `report`, `scan` or `target`
                           This param will help to determine where to search
                           for the report
        :return: `Report` object
        :example:
        ```python
            >>> report = await api.reports.get_report(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> print(report)
        ```
        """
        if isinstance(report, (Report, str)):
            try:
                return Report.from_dict(
                    await self.request("GET", f"reports/{get_input_report_id(report)}")
                )
            except Acunetix404Error:
                if not isinstance(report, str) or input_type and input_type == "report":
                    raise

        if isinstance(report, (Scan, str)):
            try:
                scan: Scan = await self.get_scan(report)
            except Acunetix404Error:
                if not isinstance(report, str) or input_type and input_type == "scan":
                    raise

            report: InputTargetType = scan.target

        if isinstance(report, (Target, str)):
            reports: typing.List[Report] = await self.get_reports()
            for _report in reports:
                if get_input_target_id(report) in _report.source.id_list:
                    return _report

        raise Acunetix404Error(404, "Report not found")

    async def create_report(
        self,
        template: InputReportTemplate,
        source: TypedList,
        done_callback: typing.Optional[CallbackFunction] = None,
    ) -> Report:
        """
        Create new report
        :param template: Report template ID or `ReportTemplate` object
        :param source: `TypedList` object
        :param done_callback: Callback function that will be called
                              when report is ready
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
        response: dict = await self.request(
            "POST",
            "reports",
            {"template_id": get_input_report_template_id(template), "source": source},
        )

        if "report_id" not in response:
            raise ValueError("Invalid response")

        if done_callback:
            self._callbacks[response["report_id"]] = done_callback

        return await self.get_report(response["report_id"])

    async def get_report_templates(self) -> typing.List[ReportTemplate]:
        """
        Get all report templates
        :return: List of `ReportTemplate` objects
        :example:
        ```python
            >>> report_templates = await api.reports.get_report_templates()
            >>> for report_template in report_templates:
            >>>     print(report_template)
        ```
        """
        return [
            ReportTemplate.from_dict(report_template)
            for report_template in (await self.request("GET", "report_templates"))[
                "report_templates"
            ]
        ]

    async def delete_reports(self, reports: typing.List[InputReport]) -> None:
        """
        Delete reports
        :param reports: List of report IDs or `Report` objects
        :return: None
        :example:
        ```python
            >>> await api.reports.delete_reports(
                    [
                        "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                        Report(...),
                    ],
                )
        ```
        """
        await self.request(
            "POST",
            "reports/delete",
            {"report_id_list": [get_input_report_id(report) for report in reports]},
        )

    async def delete_report(self, report: InputReport) -> None:
        """
        Delete report
        :param report: Report ID or `Report` object
        :return: None
        :example:
        ```python
            >>> await api.reports.delete_report(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> await api.reports.delete_report(
                    Report(...),
                )
        ```
        """
        await self.delete_reports([report])

    async def download_report(
        self,
        report: InputReport,
        download: str = "both",
    ) -> typing.List[io.BytesIO]:
        """
        Download report
        :param report: Report ID or `Report` object
        :param download: Download type. Can be `both`, `html` or `pdf`
        :return: Report content
        :example:
        ```python
            >>> report_content = await api.reports.download_report(
                    "316f58ff-f6d6-47d5-b5e3-806837a8cfe2",
                )
            >>> print(report_content)
        ```
        """
        report: Report = await self.get_report(report)
        files: typing.List[io.BytesIO] = []

        for uri in report.download:
            if download != "both" and not uri.endswith(f".{download}"):
                continue

            report_url = f"https://{self._endpoint}{uri}"
            with tempfile.TemporaryDirectory() as tmpdir:
                file = os.path.join(tmpdir, "report")
                filename: str = None

                def download_file():
                    nonlocal filename
                    with requests.get(report_url, stream=True, verify=False) as r:
                        r.raise_for_status()
                        filename = r.headers.get("Content-Disposition").split("=")[1]
                        with open(file, "wb") as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)

                await run_sync(download_file)

                async with aopen(file, "rb") as f:
                    file: io.BytesIO = io.BytesIO(await f.read())

                file.name = filename
                file.seek(0)
                files.append(file)

        return files
