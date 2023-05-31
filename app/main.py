from fastapi import FastAPI, APIRouter, status

app = FastAPI()
router = APIRouter()

@router.get("/")
def get_notes():
    return "return a list of notes"

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_note():
    return "create note item"

@router.patch("/{noteId}")
def update_note(noteId: str):
    return f"update note item with id {noteId}"

@router.get("/{noteId}")
def get_note(noteId: str):
    return f"get note item with id {noteId}"

@router.delete("/{noteId}")
def delete_note(noteId: str):
    return f"delete note item with id {noteId}"

app.include_router(router, tags=["Notes"], prefix="/api/v1/notes")

@app.get('/api/v1/healthcheck')
def healthcheck():
    return {"message": "This is fine"}