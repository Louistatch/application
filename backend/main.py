from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routes import router

app = FastAPI(
    title="Amẓarug Aqbayli n Tẓuṛt n Wakal",
    description="AI Agronomist Agent — speaks and understands Kabyle",
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
    from rag.pipeline import ingest_agro_seed_data
    from rag.retriever import KabyleRetriever
    retriever = KabyleRetriever()
    if retriever.collections["agro"].count() == 0:
        print("Seeding agro vocabulary...")
        ingest_agro_seed_data()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
