def taskEntity(task) -> dict:
    return {
        "id": str(task["_id"]),
        "description": task["description"],
        "status": task["status"],
        "createdAt": task["createdAt"],
        "updatedAt": task["updatedAt"]
    }

def taskListEntity(tasks) -> list:
    return [taskEntity(task) for task in tasks]