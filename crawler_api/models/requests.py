import re

from pydantic import BaseModel, Field, validator

LEGAL_PROCESS_NUMBER_PATTERN = re.compile(r'^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$')


class LegalProcess(BaseModel):
    number: str = Field(description='Valid format: XXXXXXXX-XX-XXXX.XX.XXXX', example='1234567-12.1234.1.12.1234')

    @validator('number')
    def check_number(cls, value):
        is_full_match = LEGAL_PROCESS_NUMBER_PATTERN.fullmatch(value.upper())
        if not is_full_match:
            raise ValueError('Invalid number format. Example: 1234567-12.1234.1.12.1234')
        return value
