from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlmodel import Session, select
from models.codes import Request_Status_Codes
from db import get_session
from typing import List
#from enums import create_dynamic_enum, get_enum_values
import pandas as pd
import io

router = APIRouter()

#Upload excel
@router.post("/upload_code_info")
async def upload_code_info(file: UploadFile = File(...), session: Session = Depends(get_session)):
    df = pd.read_excel(file.file)
    statuses = df["request_status"].dropna().unique()

    for status in statuses:
        existing = session.exec(
            select(Request_Status_Codes).where(Request_Status_Codes.request_status == status)
        ).first()
        if not existing:
            session.add(Request_Status_Codes(request_status=status))
    session.commit()


    return {"message": "Request statuses added successfully", "count": len(statuses)}
    
