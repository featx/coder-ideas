from enum import Enum


class BusinessException(Exception):
    code = 0
    message = ""
    extra = None

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def with_extra(self, extra):
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

    NOTHING_TO_GENERATE = BusinessException(code=4001000, message="Nothing to generate")


    UNAUTHORIZED = BusinessException(code=4010000, message="Authorization required")
    CREDENTIAL_INVALID = BusinessException(code=4010001, message="Credential invalid")
    AUTH_INVALID = BusinessException(code=4010002, message="Authorization invalid")


    NOT_FOUND = BusinessException(code=4040000, message="Entity not found")
    TEMPLATE_NOT_FOUND = BusinessException(code=4041001, message="template not found")
    PROJECT_NOT_FOUND = BusinessException(code=4041002, message="project not found")
    DATA_ENGINE_NOT_FOUND = BusinessException(code=4041003, message="data engine not found")
    RULE_NOT_FOUND = BusinessException(code=4041004, message="template rule not found")
    DOMAIN_NOT_FOUND = BusinessException(code=4041005, message="project domain not found")



    SYSTEM_ERROR = BusinessException(code=5000000, message="System error")

    def with_info(self, extra):
        if isinstance(self.value, BusinessException):
            return self.value.with_extra(extra)
        return None
