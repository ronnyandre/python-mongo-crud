from datetime import datetime
from fastapi import HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Note
from app.note_serializers import noteEntity, noteListEntity
from bson.objectid import ObjectId

router = APIRouter()

@router.get("/", response_model=schemas.ListNoteResponse)
def get_notes(limit: int = 10, page: int = 1, search: str = ""):
    skip = (page - 1) * limit

    pipeline = [
        {"$match": {"title": {"$regex": search, "$options": "i"}}},
        {
            "$skip": skip
        }, {
            "$limit": limit
        }
    ]

    notes = noteListEntity(Note.aggregate(pipeline))

    return {
        "status": "success",
        "results": len(notes),
        "notes": notes
    }