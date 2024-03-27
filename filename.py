from typing import Optional, Tuple, Any
from pydantic import BaseModel, PositiveInt, field_validator
from datetime import datetime


class Filename(BaseModel, validate_assignment=True):
    base_name: str
    ext: str
    created_at: datetime
    resolution: Optional[Tuple[PositiveInt, PositiveInt]] = None
    pre: Optional[str] = ''
    post: Optional[str] = ''

    @field_validator('created_at')
    @classmethod
    def parse_date(cls, ca: Any):
        if isinstance(ca, datetime):
            return ca
        elif isinstance(ca, str):
            try:
                return datetime.strptime(ca, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        else:
            raise TypeError("created_at must be a datetime or string")
