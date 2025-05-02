from sqlmodel import SQLModel, Field
from typing import Optional

class Request_Status_Codes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_status: str = Field(index=True, unique=True, max_length=50)