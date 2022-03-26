from datetime import date
from pydantic import BaseModel


class ConversionResult(BaseModel):
    from_currency: str
    to_currency: str
    query_amount: float
    timestamp: str
    rate: float
    coversion_rate: float