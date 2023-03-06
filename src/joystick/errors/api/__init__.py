from ..joystick_error import JoystickError


class ApiHttpError(JoystickError):
    pass


class BadRequestError(ApiHttpError):
    pass


class ServerError(ApiHttpError):
    pass


class UnknownError(ApiHttpError):
    pass


class ApiError(JoystickError):
    pass


class MultipleContentsApiError(ApiError):
    pass
