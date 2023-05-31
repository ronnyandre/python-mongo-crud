from datetime import datetime
from fastapi import HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Note
from app.note_serializers import noteEntity, noteListEntity
from bson.objectid import ObjectId

router = APIRouter()

# Function to check if ID exists
def check_if_id_exists(id: str):
     if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid note ID {id}")

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

    # Set create and update datetime
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

# [...] Update a record
@router.patch("/{noteId}", response_model=schemas.NoteResponse)
def update_note(noteId: str, payload: schemas.UpdateNoteSchema):

    # Check if ID exists
    check_if_id_exists(noteId)

    # Convert to dictionary and update datetime
    note_dict = payload.dict(exclude_none=True)
    note_dict["updatedAt"] = datetime.utcnow()
    
    # Update in database
    updated_note = Note.find_one_and_update(
        {"_id": ObjectId(noteId)},
        {"$set": note_dict},
        return_document=ReturnDocument.AFTER
    )

    if not updated_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with ID {noteId} does not exist")
    
    return {
        "status": "success",
        "note": noteEntity(updated_note)
    }

# [...] Get a single record
@router.get("/{noteId}", response_model=schemas.NoteResponse)
def get_note(noteId: str):

    # Check if ID exists
    check_if_id_exists(noteId)

    note = Note.find_one({"_id": ObjectId(noteId)})

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with ID {noteId} does not exist")
    
    return {
        "status": "success",
        "note": noteEntity(note)
    }

# [...] Delete a record
@router.delete("/{noteId}")
def delete_note(noteId: str):
    
    # Check if ID exists
    check_if_id_exists(noteId)

    note = Note.find_one_and_delete({"_id": ObjectId(noteId)})

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with ID {noteId} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)