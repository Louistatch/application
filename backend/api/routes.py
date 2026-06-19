from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
import langdetect

from api.schemas import (
    ChatRequest, ChatResponse,
    TranslationRequest, TranslationResponse,
    IngestRequest,
)
from agent.kabye_agent import KabyeAgroAgent

router = APIRouter()
_agent = None


def get_agent() -> KabyeAgroAgent:
    global _agent
    if _agent is None:
        _agent = KabyeAgroAgent()
    return _agent


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        lang = None
        try:
            lang = langdetect.detect(req.message)
        except Exception:
            pass

        history = [{"role": m.role, "content": m.content} for m in req.history]
        reply = get_agent().chat(req.message, history)
        return ChatResponse(reply=reply, language_detected=lang)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    history = [{"role": m.role, "content": m.content} for m in req.history]

    def generator():
        for chunk in get_agent().stream_chat(req.message, history):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream")


@router.post("/translate", response_model=TranslationResponse)
async def translate(req: TranslationRequest):
    try:
        result = get_agent().translate(req.text, req.direction)
        return TranslationResponse(
            original=req.text,
            translated=result,
            direction=req.direction,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest")
async def ingest(req: IngestRequest):
    from rag.pipeline import ingest_dictionary, ingest_audio, ingest_agro_seed_data
    try:
        if req.type == "seed":
            ingest_agro_seed_data()
            return {"status": "ok", "message": "Agro seed data indexed."}
        elif req.type == "dictionary":
            if not req.file_path:
                raise HTTPException(status_code=400, detail="file_path required")
            ingest_dictionary(req.file_path)
            return {"status": "ok", "message": f"Dictionary {req.file_path} indexed."}
        elif req.type == "audio":
            if not req.file_path:
                raise HTTPException(status_code=400, detail="file_path required")
            ingest_audio(req.file_path)
            return {"status": "ok", "message": f"Audio {req.file_path} transcribed and indexed."}
        else:
            raise HTTPException(status_code=400, detail="type must be: seed | dictionary | audio")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/dictionary")
async def upload_dictionary(file: UploadFile = File(...)):
    import shutil, os
    dest = f"./data/raw/{file.filename}"
    os.makedirs("./data/raw", exist_ok=True)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    from rag.pipeline import ingest_dictionary
    ingest_dictionary(dest)
    return {"status": "ok", "file": dest}


@router.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    import shutil, os
    dest = f"./data/raw/{file.filename}"
    os.makedirs("./data/raw", exist_ok=True)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    from rag.pipeline import ingest_audio
    ingest_audio(dest)
    return {"status": "ok", "file": dest}


@router.get("/health")
async def health():
    return {"status": "ok", "agent": "Agronome Kabyè — Togo Nord"}
