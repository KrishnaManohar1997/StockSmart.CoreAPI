from enum import Enum


class BaseEnum(Enum):
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.value

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
