from enum import Enum


class BusinessException(Exception):
    code = 0
    message = ""
    extra = None

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def and_with(self, extra):
        self.extra = extra
        return self

    def set_code(self, code: int):
        self.code = code
        return self

    def set_message(self, message: str):
        self.message = message
        return self


class BusinessError(Enum):
    PARAMETER_LOST = BusinessException(code=4000010, message="Parameter lost")
    PARAMETER_TYPE = BusinessException(code=4000011, message="Parameter type error")
    PARAMETER_INVALID = BusinessException(code=4000012, message="Parameter invalid")

    UNAUTHORIZED = BusinessException(code=4010000, message="Authorization required")
    CREDENTIAL_INVALID = BusinessException(code=4010001, message="Credential invalid")
    AUTH_INVALID = BusinessException(code=4010002, message="Authorization invalid")

    NOT_FOUND = BusinessException(code=4040000, message="Entity not found")
    PROJECT_NOT_FOUND = BusinessException(code=4041001, message="project not found")
    DATA_ENGINE_NOT_FOUND = BusinessException(code=4041002, message="data engine not found")

    SYSTEM_ERROR = BusinessException(code=5000000, message="System error")

