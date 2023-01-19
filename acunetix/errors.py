class AcunetixAPIError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message

    def __str__(self):
        return (
            f"Got response with status code {self.status} from Acunetix: {self.message}"
        )


class Acunetix404Error(AcunetixAPIError):
    pass


class Acunetix401Error(AcunetixAPIError):
    pass


class Acunetix400Error(AcunetixAPIError):
    pass


class Acunetix500Error(AcunetixAPIError):
    pass


class Acunetix503Error(AcunetixAPIError):
    pass


class Acunetix504Error(AcunetixAPIError):
    pass


class Acunetix429Error(AcunetixAPIError):
    pass


class Acunetix403Error(AcunetixAPIError):
    pass


class Acunetix409Error(AcunetixAPIError):
    pass


class Acunetix422Error(AcunetixAPIError):
    pass


class Acunetix502Error(AcunetixAPIError):
    pass


ERROR_MAP = {
    404: Acunetix404Error,
    401: Acunetix401Error,
    400: Acunetix400Error,
    500: Acunetix500Error,
    503: Acunetix503Error,
    504: Acunetix504Error,
    429: Acunetix429Error,
    403: Acunetix403Error,
    409: Acunetix409Error,
    422: Acunetix422Error,
    502: Acunetix502Error,
}
