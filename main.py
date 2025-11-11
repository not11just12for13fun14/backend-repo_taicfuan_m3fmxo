import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Baby, Milestone, Growthrecord

app = FastAPI(title="Baby Development Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helpers

def to_str_id(doc):
    if not doc:
        return doc
    d = dict(doc)
    if d.get("_id"):
        d["id"] = str(d.pop("_id"))
    return d

class CreateBabyResponse(BaseModel):
    id: str

@app.get("/")
def read_root():
    return {"message": "Baby Development Tracker API"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response

# Babies
@app.post("/api/babies", response_model=CreateBabyResponse)
def create_baby(payload: Baby):
    try:
        new_id = create_document("baby", payload)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/babies")
def list_babies():
    try:
        docs = get_documents("baby")
        return [to_str_id(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Milestones
@app.post("/api/milestones")
def add_milestone(payload: Milestone):
    try:
        new_id = create_document("milestone", payload)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/milestones")
def list_milestones(baby_id: Optional[str] = None):
    try:
        filt = {"baby_id": baby_id} if baby_id else {}
        docs = get_documents("milestone", filt)
        return [to_str_id(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Growth records
@app.post("/api/growth")
def add_growth(payload: Growthrecord):
    try:
        new_id = create_document("growthrecord", payload)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/growth")
def list_growth(baby_id: Optional[str] = None):
    try:
        filt = {"baby_id": baby_id} if baby_id else {}
        docs = get_documents("growthrecord", filt)
        return [to_str_id(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
