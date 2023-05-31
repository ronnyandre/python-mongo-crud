from datetime import datetime
from fastapi import HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Task
from app.task_serializers import taskEntity, taskListEntity
from bson.objectid import ObjectId

router = APIRouter()

# Function to check if ID exists
def check_if_id_exists(id: str):
     if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid task ID {id}")

# [...] Get 10 first records
@router.get("/", response_model=schemas.ListTaskResponse)
def get_tasks(limit: int = 10, page: int = 1, search: str = ""):
    skip = (page - 1) * limit

    pipeline = [
        {"$match": {"description": {"$regex": search, "$options": "i"}}},
        {
            "$skip": skip
        }, {
            "$limit": limit
        }
    ]

    tasks = taskListEntity(Task.aggregate(pipeline))

    return {
        "status": "success",
        "results": len(tasks),
        "tasks": tasks
    }

# [...] Create a record
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskResponse)
def create_task(payload: schemas.TaskBaseSchema):

    # Set create and update datetime
    payload.createdAt = datetime.utcnow()
    payload.updatedAt = payload.createdAt

    try:
        result = Task.insert_one(payload.dict(exclude_none=True))
        new_task = Task.find_one({"_id": result.inserted_id})

        return {
            "status": "success",
            "task": taskEntity(new_task)
        }
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Task could not be created")
