import asyncio
import inspect
import io
import json
import logging
import string
import typing

import requests
import urllib3

from . import errors, methods, schema, status_codes, typehints, utils
from .errors import (
    ERROR_MAP,
    Acunetix400Error,
    Acunetix401Error,
    Acunetix403Error,
    Acunetix404Error,
    Acunetix409Error,
    Acunetix422Error,
    Acunetix429Error,
    Acunetix500Error,
    Acunetix502Error,
    Acunetix503Error,
    Acunetix504Error,
    AcunetixAPIError,
)
from .methods import Reports, Scans, Targets, Users
from .schema import (
    AFFECTED_ITEMS,
    COMPREHENSIVE,
    CRAWL_ONLY,
    CWE_SANS_TOP_25,
    DEVELOPER,
    EXECUTIVE_SUMMARY,
    FULL_SCAN,
    HIGH_OR_MEDIUM_RISK_VULNERABILITIES,
    HIGH_RISK_VULNERABILITIES,
    HIPAA,
    ISO_27001,
    MALWARE_SCAN,
    NIST_SP800_53,
    OWASP_TOP_10_2013,
    OWASP_TOP_10_2017,
    OWASP_TOP_10_2021,
    PCI_DSS_3_2,
    QUICK,
    SARBANES_OXLEY,
    SCAN_COMPARISON,
    SCAN_PROFILE_MAP,
    SQL_INJECTION_VULNERABILITIES,
    STIG_DISA,
    TEMPLATE_MAP,
    WASC_THREAT_CLASSIFICATION,
    WEAK_PASSWORDS,
    XSS_VULNERABILITIES,
    AccessMap,
    FileAttachment,
    Host,
    InputTarget,
    Message,
    Notification,
    NotificationData,
    Report,
    ReportTemplate,
    Scan,
    ScanSpeed,
    StatusStatisticEntry,
    StatusStatistics,
    Target,
    TargetHostInfo,
    TargetInfo,
    TypedList,
    User,
    Vulnerability,
    WebScanStatus,
    WebVulnerabilityScanner,
)
from .status_codes import EXPORT_DONE_STATUS, REPORT_DONE_STATUS, SCAN_DONE_STATUS
from .typehints import (
    CallbackFunction,
    InputReport,
    InputReportTemplate,
    InputScan,
    InputScanProfile,
    InputTargetType,
    InputUser,
)

__all__ = [
    "AcunetixAPI",
    "AcunetixAPIError",
    "Acunetix400Error",
    "Acunetix401Error",
    "Acunetix403Error",
    "Acunetix404Error",
    "Acunetix409Error",
    "Acunetix422Error",
    "Acunetix429Error",
    "Acunetix500Error",
    "Acunetix502Error",
    "Acunetix503Error",
    "Acunetix504Error",
    "ERROR_MAP",
    "EXPORT_DONE_STATUS",
    "FileAttachment",
    "InputTarget",
    "Notification",
    "NotificationData",
    "REPORT_DONE_STATUS",
    "Report",
    "SCAN_DONE_STATUS",
    "Scan",
    "Target",
    "status_codes",
    "methods",
    "schema",
    "errors",
    "TypedList",
    "User",
    "AccessMap",
    "ReportTemplate",
    "DEVELOPER",
    "QUICK",
    "EXECUTIVE_SUMMARY",
    "HIPAA",
    "AFFECTED_ITEMS",
    "SCAN_COMPARISON",
    "CWE_SANS_TOP_25",
    "ISO_27001",
    "NIST_SP800_53",
    "OWASP_TOP_10_2013",
    "OWASP_TOP_10_2017",
    "OWASP_TOP_10_2021",
    "PCI_DSS_3_2",
    "SARBANES_OXLEY",
    "STIG_DISA",
    "WASC_THREAT_CLASSIFICATION",
    "TEMPLATE_MAP",
    "InputReport",
    "InputScan",
    "InputTargetType",
    "InputReportTemplate",
    "InputUser",
    "CallbackFunction",
    "FULL_SCAN",
    "HIGH_RISK_VULNERABILITIES",
    "HIGH_OR_MEDIUM_RISK_VULNERABILITIES",
    "XSS_VULNERABILITIES",
    "SQL_INJECTION_VULNERABILITIES",
    "WEAK_PASSWORDS",
    "CRAWL_ONLY",
    "MALWARE_SCAN",
    "InputScanProfile",
    "SCAN_PROFILE_MAP",
    "COMPREHENSIVE",
    "Host",
    "Message",
    "StatusStatisticEntry",
    "StatusStatistics",
    "TargetHostInfo",
    "TargetInfo",
    "Vulnerability",
    "WebScanStatus",
    "WebVulnerabilityScanner",
    "Users",
    "utils",
    "typehints",
    "ScanSpeed",
]

logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return (
            obj.to_json()
            if hasattr(obj, "to_json")
            else json.JSONEncoder.default(self, obj)
        )


class AcunetixAPI(Scans, Targets, Reports, Users):
    """
    Acunetix API client.
    You must deploy your own Acunetix instance to use this client.
    """

    def __init__(self, api_key: str, endpoint: str = "localhost:3443"):
        """
        :param api_key: API key from Acunetix
        :param endpoint: Acunetix API endpoint. Default is localhost:3443
        :example:
        ```python
            >>> api = AcunetixAPI(
                    "1986ad8c0a5b3df4d7028d5f3c06e946cdcc13b0d336841bc93daf7e58fb8a63a",
                )
        ```
        """
        if not api_key or any(char not in string.hexdigits for char in api_key):
            raise ValueError("Invalid API key")

        if not endpoint:
            raise ValueError("Invalid endpoint")

        self._api_key: str = api_key
        self._endpoint: str = endpoint
        self._callbacks: dict = {}
        self._connected: bool = False

    async def connect(self, no_credentials_check: bool = False):
        """
        Connect to Acunetix API. Required before using any other methods.
        Without calling it, the credentials will be checked only when the
        first request is made. Also, callbacks will not be executed.
        :example:
        ```python
            >>> await api.connect()
            ```
        """
        if self._connected:
            return

        self._connected = True

        logger.debug("Connecting...")
        if not no_credentials_check:
            await self._check_credentials()

        logger.debug("Connected")

        asyncio.create_task(self._poll_notifications())

    async def _execute_callback(self, callback_id: str, notification: Notification):
        """
        Executes a callback if it exists
        :param callback_id: Callback ID
        :param notification: Notification
        """
        if callback_id not in self._callbacks:
            return

        logger.debug("Executing callback for %s", callback_id)

        callback: typing.Callable = self._callbacks.pop(callback_id)
        callback: typing.Union[typing.Awaitable, typing.Any] = (
            callback(notification)
            if inspect.signature(callback).parameters
            else callback()
        )

        if asyncio.iscoroutinefunction(callback):
            await callback

    async def _poll_notifications(self):
        """Polls the Acunetix API for notifications"""
        while True:
            try:
                notifications: dict = await self.request("GET", "notifications")
                for notification in notifications["notifications"]:
                    logger.debug(
                        "Processing notification %s",
                        notification["notification_id"],
                    )
                    if notification["type_id"] in SCAN_DONE_STATUS + REPORT_DONE_STATUS:
                        logger.debug(
                            "Executing callback for %s",
                            notification["resource_id"],
                        )
                        await self._execute_callback(
                            notification["resource_id"],
                            Notification.from_dict(notification),
                        )

                    await self.request(
                        "POST",
                        f"notifications/{notification['notification_id']}/consume",
                    )

            except AcunetixAPIError as e:
                logger.exception(e)

            await asyncio.sleep(5)

    async def request(
        self,
        method: str,
        path: str,
        data: dict = None,
        full_response: bool = False,
    ) -> typing.Union[dict, requests.Response]:
        """
        Makes a request to the Acunetix API
        :param method: HTTP method
        :param path: API path
        :param data: JSON data
        :param full_response: If True, returns the full response object
        :return: JSON response or full response object
        """
        logger.debug("Requesting %s %s", method, path)
        response: requests.Response = await utils.run_sync(
            lambda: requests.request(
                method,
                f"https://{self._endpoint}/api/v1/{path}",
                data=json.dumps(data, cls=CustomJSONEncoder),
                headers={"X-Auth": self._api_key, "Content-Type": "application/json"},
                verify=False,
            )
        )
        if response.status_code == 204:
            return {}

        if response.status_code not in range(200, 300):
            raise ERROR_MAP.get(response.status_code, AcunetixAPIError)(
                response.status_code,
                response.text,
            )

        return response if full_response else response.json()

    async def _check_credentials(self):
        """Checks if the credentials are valid"""
        await self.request("GET", "me")

    async def default_scan(
        self,
        target: InputTarget,
        scan_profile: InputScanProfile = FULL_SCAN,
        report_template: InputReportTemplate = DEVELOPER,
        download: str = "both",
        scan_speed: str = ScanSpeed.FAST,
    ) -> typing.List[io.BytesIO]:
        """
        Performs a default scan on a target
        :param target: Target
        :param scan_profile: Scan profile
        :param report_template: Report template
        :param download: Download type. Can be "both", "pdf" or "html"
        :param scan_speed: Scan speed
        :return: List of reports as PDF files objects
        :example:
        ```python
            >>> import os
            >>> target = InputTarget(
                    target="http://example.com",
                    description="Example target",
                )
            >>> files = await api.default_scan(target)
            >>> for file in files:
            >>>     with open(os.path.join("reports", file.name), "wb") as f:
            >>>         f.write(file.read())
            >>> print(os.listdir("reports"))
        ```
        """
        logger.debug("Creating target %s", target)
        target: Target = await self.create_target(target)
        done_event: asyncio.Event = asyncio.Event()
        await self.set_scan_speed(target, scan_speed)

        logger.debug("Performing scan on %s", target.target_id)
        scan: Scan = await self.create_scan(
            target,
            scan_profile,
            # If we generate report here, we won't be able to attach callback
            # to it. This is how Acunetix works. That's why we omit
            # default report creation here and create it manually later.
            None,
            None,
            done_event.set,
        )
        await done_event.wait()

        logger.debug("Retrieving scan results %s", scan.scan_id)
        scan = await self.get_scan(scan)
        done_event.clear()

        logger.debug("Creating report for %s", scan.scan_id)
        report: Report = await self.create_report(
            report_template,
            TypedList("scans", [scan.scan_id]),
            done_event.set,
        )
        await done_event.wait()

        logger.debug("Retrieving report %s", report.report_id)
        files: typing.List[io.BytesIO] = await self.download_report(report, download)

        logger.debug("Report ready %s", report.report_id)
        return files
