from app import note, task
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

api_version = "v1"

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(note.router, tags=["Notes"], prefix=f"/api/{api_version}/notes")
app.include_router(task.router, tags=["Tasks"], prefix=f"/api/{api_version}/tasks")

@app.get(f"/api/{api_version}/healthcheck")
def healthcheck():
    return {"message": "This is fine"}