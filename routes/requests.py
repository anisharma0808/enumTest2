from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlmodel import Session, select
from typing import List
from models.requests_model import s_requests
from models.codes import Request_Status_Codes
from db import get_session

router = APIRouter()

# Fetch all records from sf_bom_predict_requests
@router.get("/requests", response_model=List[s_requests])
def get_all_data(db: Session = Depends(get_session)):
    return db.exec(select(s_requests)).all()

# Insert a new record from sf_bom_predict_requests
@router.post("/requests", response_model=s_requests)
def add_data(entry: s_requests, db: Session = Depends(get_session)):
    valid_status = db.exec(
        select(Request_Status_Codes).where(Request_Status_Codes.request_status == entry.request_status)
    ).first()

    if not valid_status:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request_status '{entry.request_status}'. Must be one of the defined Request_Status_Codes."
        )

    dataset = s_requests.from_orm(entry)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset