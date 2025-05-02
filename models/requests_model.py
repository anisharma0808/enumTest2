from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

#s_requests(Slide 6)
class s_requests_base(SQLModel):
    bom_id: str = Field(max_length=50)
    target_project:	str = Field(max_length=50)
    source_project:	Optional[str] = Field(default=None, max_length=50)
    requested_by: str = Field(max_length=50)
    requested_on: Optional[date] = Field(default=None)
    request_status: str = Field(max_length=50)

class s_requests(s_requests_base, table=True):
    bom_id: str = Field(primary_key=True, max_length=50)