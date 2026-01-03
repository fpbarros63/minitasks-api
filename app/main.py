from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers.health import router as health_router
from app.routers.tasks import router as tasks_router
from app.exceptions import NotFoundError


openapi_tags = [
    {
        "name": "Tasks (Collection)",
        "description": "Operations over the tasks collection (create and list tasks).",
    },
    {
        "name": "Tasks (Item)",
        "description": "Operations over a single task resource (get, update, delete).",
    },
    {
        "name": "Health",
        "description": "Service health check endpoints.",
    },
]

app = FastAPI(
    title="MiniTasks API",
    openapi_tags=openapi_tags,
)


# Routers
app.include_router(health_router)
app.include_router(tasks_router)


# Exception handlers
@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "type": "not_found",
                "message": exc.message,
                "path": str(request.url.path),
            }
        },
    )
