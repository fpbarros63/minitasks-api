from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.tasks import router as tasks_router
from app.database import engine
from app.models import Base

from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions import NotFoundError

app = FastAPI(title="MiniTasks API")

app.include_router(health_router)
app.include_router(tasks_router)

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

