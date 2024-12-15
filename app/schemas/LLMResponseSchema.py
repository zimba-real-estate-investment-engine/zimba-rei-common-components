import json
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LLMResponseSchema(BaseModel):

    id: Optional[int] = None
    listing_url:  str
    listing_raw_text:  str
    llm_service_api_url:  str
    llm_service_prompt:  str
    llm_response_json:  str
    created_date: datetime = None

    class Config:
        orm_mode = True
        from_attributes = True
