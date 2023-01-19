import asyncio
import json
import logging
import string

import aiohttp

from . import errors, methods, schema, status_codes
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
from .methods import Reports, Scans, Targets
from .schema import (
    FileAttachment,
    InputTarget,
    Notification,
    NotificationData,
    Report,
    Scan,
    Target,
)
from .status_codes import (
    EXPORT_DONE_STATUS,
    REPORT_DONE_STATUS,
    SCAN_DONE_STATUS,
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
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _default(self, obj):  # skipcq: PYL-W0613
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = json.JSONEncoder().default
json.JSONEncoder.default = _default


class AcunetixAPI(Scans, Targets, Reports):
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

        self._api_key = api_key
        self._endpoint = endpoint
        self._callbacks = {}
        self._connected = False

    async def connect(self):
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
        await self._check_credentials()
        asyncio.create_task(self._poll_notifications())

    async def _execute_callback(self, callback_id: str, notification: Notification):
        if callback_id not in self._callbacks:
            return

        callback = self._callbacks.pop(callback_id)(notification)
        if asyncio.iscoroutinefunction(callback):
            await callback

    async def _poll_notifications(self):
        while True:
            try:
                notifications = await self._request("GET", "notifications")
                for notification in notifications["notifications"]:
                    logger.debug(
                        "Processing notification %s", notification["notification_id"]
                    )
                    if notification["type_id"] in SCAN_DONE_STATUS + REPORT_DONE_STATUS:
                        logger.debug(
                            "Executing callback for %s", notification["resource_id"]
                        )
                        await self._execute_callback(
                            notification["resource_id"],
                            Notification.from_dict(notification),
                        )

                    await self._request(
                        "POST",
                        f"notifications/{notification['notification_id']}/consume",
                    )

            except AcunetixAPIError as e:
                logger.exception(e)

            await asyncio.sleep(5)

    async def _request(
        self,
        method: str,
        path: str,
        data: dict = None,
        full_response: bool = False,
    ):
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                f"https://{self._endpoint}/api/v1/{path}",
                json=data,
                headers={"X-Auth": self._api_key},
            ) as response:
                if response.status == 204:
                    return {}

                if response.status not in range(200, 300):
                    raise ERROR_MAP.get(response.status, AcunetixAPIError)(
                        response.status,
                        await response.text(),
                    )

                return response if full_response else await response.json()

    async def _check_credentials(self):
        await self._request("GET", "me")
        logger.info("Connected")
