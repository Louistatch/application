import anthropic

from config import settings
from agent.prompts import SYSTEM_PROMPT_KABYE as SYSTEM_PROMPT_KABYE, TRANSLATION_PROMPT


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
            prompt = f"Traduis ce texte français en kabyè (avec translittération):\n\n{text}"
        else:
            prompt = f"Traduis ce texte kabyè en français:\n\n{text}"

        context = self._build_context(text)
        system = TRANSLATION_PROMPT
        if context:
            system += f"\n\nIsallen n umawal:\n{context}"

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
