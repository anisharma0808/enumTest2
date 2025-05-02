import io
import pandas as pd
from datetime import date

def test_upload_code_info(client):
    df = pd.DataFrame({"request_status": ["Pending", "Approved"]})
    file = io.BytesIO()
    with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    file.seek(0)

    response = client.post("/upload_code_info", files={"file": ("test.xlsx", file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")})
    assert response.status_code == 200
    assert response.json()["count"] == 2

def test_add_data_success(client):
    payload = {
        "bom_id": "BOM001",
        "target_project": "TP1",
        "source_project": "SP1",
        "requested_by": "User1",
        "requested_on": str(date.today()),
        "request_status": "Pending"
    }

    response = client.post("/requests", json=payload)
    assert response.status_code == 200
    assert response.json()["bom_id"] == "BOM001"

def test_add_data_invalid_status(client):
    payload = {
        "bom_id": "BOM002",
        "target_project": "TP2",
        "source_project": "SP2",
        "requested_by": "User2",
        "requested_on": str(date.today()),
        "request_status": "InvalidStatus"
    }

    response = client.post("/requests", json=payload)
    assert response.status_code == 400
    assert "Invalid request_status" in response.json()["detail"]

def test_get_all_requests(client):
    response = client.get("/requests")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

def test_get_enum_values(client):
    response = client.get("/status_enum/")
    assert response.status_code == 200
    assert "Pending" in response.json()