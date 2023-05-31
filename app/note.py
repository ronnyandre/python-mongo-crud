from datetime import datetime
from fastapi import HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Note
from app.note_serializers import noteEntity, noteListEntity
from bson.objectid import ObjectId

router = APIRouter()

# [...] Get 10 first records
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

# [...] Create a record
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.NoteResponse)
def create_note(payload: schemas.NoteBaseSchema):
    payload.createdAt = datetime.utcnow()
    payload.updatedAt = payload.createdAt

    try:
        result = Note.insert_one(payload.dict(exclude_none=True))
        new_note = Note.find_one({"_id": result.inserted_id})

        return {
            "status": "success",
            "note": noteEntity(new_note)
        }
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Note with title {payload.title} already exists")
    