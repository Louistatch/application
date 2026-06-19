from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routes import router

app = FastAPI(
    title="Agronome Kabyè — Agriculture Togo Nord",
    description="AI Agronomist Agent — speaks and understands Kabyè",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    print("Agronome Kabyè (Togo Nord) — ready.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
