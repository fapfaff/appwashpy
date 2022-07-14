class BaseError(Exception):
    detail = None

    def __init__(self, detail: str):
        self.detail = detail

    def to_representation(self):
        return self.detail

    def __str__(self):
        return self.to_representation()

    def __repr__(self):
        return self.to_representation()


class AppWashApiError(BaseError):
    error_code: str
    error_message: str

    def __init__(self, error_code: str, error_message: str):
        super().__init__(f"{error_code}: {error_message}")


class WrongCredentialsError(AppWashApiError):
    email: str
    password: str

    def __init__(self, error_code: str, error_message: str, email: str, password: str):
        super().__init__(error_code, error_message)
        self.email = email,
        self.password = password
