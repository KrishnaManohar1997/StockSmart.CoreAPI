from enum import Enum


class BaseChoiceTypeEnum(Enum):
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
