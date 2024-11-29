from typing import List, Optional

from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    to_addresses: List[EmailStr]
    subject: str
    body_text: str
    body_html: Optional[str] = None
    sender: Optional[EmailStr] = None

    class Config:
        orm_mode = True
