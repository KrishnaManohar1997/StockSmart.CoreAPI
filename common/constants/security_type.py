from .base_choice_enum import BaseChoiceTypeEnum


class SecurityType(BaseChoiceTypeEnum):
    EQUITY = "Equity"
    DEBT = "Debt"
    DERIVATIVES = "Derivatives"
