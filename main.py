from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Financial Compliance Superintelligence API — Constitutional Compliance Infrastructure",
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "operational", "system": settings.APP_NAME, "version": settings.VERSION}
