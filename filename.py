from typing import Optional, Tuple, Union
from pydantic import BaseModel, PositiveInt, field_validator
from datetime import datetime


class Filename(BaseModel, validate_assignment=True):
    base_name: str
    ext: str
    created_at: datetime
    resolution: Optional[Tuple[PositiveInt, PositiveInt]] = None
    pre: Optional[str] = None
    post: Optional[str] = None

    @field_validator('created_at')
    @classmethod
    def parse_date(cls, ca):
        if isinstance(ca, datetime):
            return ca
        elif isinstance(ca, str):
            try:
                return datetime.strptime(ca, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        else:
            raise TypeError("created_at must be a datetime or string")
