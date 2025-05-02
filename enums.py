from fastapi import Depends, APIRouter
from enum import Enum
from sqlmodel import Session, select
from db import get_session
from models.codes import Request_Status_Codes

router = APIRouter()

#Creating dynamic enum
def create_dynamic_enum(session: Session):
    result = session.exec(select(Request_Status_Codes)).all()
    if not result:
        return Enum("requestStatusEnum", {"DEFAULT": "No Statuses Found"})
    
    enum_dict = {
        str(item.request_status).upper().replace(" ", "_"): item.request_status
        for item in result
    }
    return Enum("requestStatusEnum", enum_dict)

@router.get("/status_enum/")
def get_enum_values(session: Session = Depends(get_session)):
    requestStatusEnum = create_dynamic_enum(session)
    return [e.value for e in requestStatusEnum]

''' Generate enum from DB values
with get_session() as session:
    rows = session.exec(select(Codes.generation).distinct()).all()
    values = [r[0] for r in rows if r and r[0]]
    if not values:
        values = ["Undefined"]

    GenerationEnum = Enum("GenerationEnum", {v.replace(" ", "_"): v for v in values})
'''