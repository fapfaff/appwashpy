from enum import Enum


class BaseEnum(Enum):
    """Modified Enum
    Allows accessing the value without .value.
    Allows == comparison
    Allows (x in BaseEnum)"""

    def __str__(self):
        """Access the value with ENUM.X instead of ENUM.X.value."""
        return self.value

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        else:
            return False

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class HTTP_METHOD(BaseEnum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'
