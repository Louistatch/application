import anthropic

from config import settings
from agent.prompts import SYSTEM_PROMPT_KABYE as SYSTEM_PROMPT_KABYE, TRANSLATION_PROMPT

_nllb_tokenizer = None
_nllb_model = None

NLLB_MODEL_ID = "facebook/nllb-200-distilled-600M"
LANG_FR  = "fra_Latn"
LANG_KBP = "kbp_Latn"


def _get_nllb():
    global _nllb_tokenizer, _nllb_model
    if _nllb_tokenizer is None:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        _nllb_tokenizer = AutoTokenizer.from_pretrained(NLLB_MODEL_ID)
        _nllb_model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_MODEL_ID)
    return _nllb_tokenizer, _nllb_model


def nllb_translate(text: str, src: str, tgt: str, max_length: int = 512) -> str:
    tok, model = _get_nllb()
    tok.src_lang = src
    inputs = tok(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    tgt_id = tok.convert_tokens_to_ids(tgt)
    out = model.generate(**inputs, forced_bos_token_id=tgt_id, max_length=max_length)
    return tok.decode(out[0], skip_special_tokens=True)


class KabyeAgroAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model
        self._retriever = None

    def _get_retriever(self):
        if self._retriever is None:
            from rag.retriever import KabyeRetriever
            self._retriever = KabyeRetriever()
        return self._retriever

    def _build_context(self, query: str) -> str:
        try:
            docs = self._get_retriever().retrieve(query, n_results=5)
        except Exception:
            return ""
        if not docs:
            return ""
        parts = ["Isallen n umawal d corpus (contexte RAG):"]
        for doc in docs:
            parts.append(f"- {doc['content']}")
        return "\n".join(parts)

    def chat(self, message: str, history: list[dict]) -> str:
        context = self._build_context(message)
        system = SYSTEM_PROMPT_KABYE
        if context:
            system += f"\n\n{context}"

        messages = history + [{"role": "user", "content": message}]
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system,
            messages=messages,
        )
        return response.content[0].text

    def stream_chat(self, message: str, history: list[dict]):
        context = self._build_context(message)
        system = SYSTEM_PROMPT_KABYE
        if context:
            system += f"\n\n{context}"

        messages = history + [{"role": "user", "content": message}]
        with self.client.messages.stream(
            model=self.model,
            max_tokens=2048,
            system=system,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield text

    def translate(self, text: str, direction: str = "fr_to_kab") -> str:
        if direction == "fr_to_kab":
            return nllb_translate(text, src=LANG_FR, tgt=LANG_KBP)
        else:
            return nllb_translate(text, src=LANG_KBP, tgt=LANG_FR)
