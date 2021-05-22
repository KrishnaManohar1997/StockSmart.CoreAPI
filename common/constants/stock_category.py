from .base_choice_enum import BaseChoiceTypeEnum


class StockCategory(BaseChoiceTypeEnum):
    SIMPLE = "Simple"
    FINANCIAL = "Financial"
    UTILITY = "Utility"
    CONSUMER_DISCRETIONARY = "ConsumerDiscretionary"
    ENERGY = "Energy"
    HEALTHCARE = "Healthcare"
    INDUSTRIAL = "Industrial"
    TECHNOLOGY = "Technology"
    TELECOM = "Telecom"
    MATERIAL = "Material"
    REAL_ESTATE = "RealEstate"
