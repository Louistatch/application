from pydantic import BaseModel


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[Message] = []


class ChatResponse(BaseModel):
    reply: str
    language_detected: str | None = None


class TranslationRequest(BaseModel):
    text: str
    direction: str = "fr_to_kab"  # "fr_to_kab" or "kab_to_fr"


class TranslationResponse(BaseModel):
    original: str
    translated: str
    direction: str


class IngestRequest(BaseModel):
    type: str  # "dictionary" | "audio" | "seed"
    file_path: str | None = None
