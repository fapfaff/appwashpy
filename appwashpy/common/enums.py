from enum import Enum, auto


class BaseStringEnum(Enum):
    """Modified Enum
    Allows == comparison
    Allows (x in BaseEnum)"""

    def __str__(self):
        """Print the value with ENUM.X instead of ENUM.X.value."""
        return self.name

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif isinstance(other, str):
            return str(self.name) == other
        else:
            return False

    @classmethod
    def has(cls, name):
        return name in cls.__members__


class HTTP_METHOD(BaseStringEnum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()


class SERVICE_TYPE(BaseStringEnum):
    WASHING_MACHINE = auto()
    DRYER = auto()
    ELECTRICITY = auto()


class STATE(BaseStringEnum):
    AVAILABLE = auto()
    OCCUPIED = auto()
    FAULTED = auto()
    SESSION_WAIT_ON = auto()
    STOPPABLE = auto()


class LOCATION_TYPE(BaseStringEnum):
    APARTMENT_BUILDING = auto()
    CAMPSITE = auto()
    HOTEL = auto()
    LAUNDROMAT = auto()
    SENIOR_RESIDENCE = auto()
    SERVICED_APARTMENT = auto()
    STUDENT_HOME = auto()
    OTHER = auto()
