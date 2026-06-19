import anthropic
from typing import AsyncGenerator

from config import settings
from agent.prompts import SYSTEM_PROMPT_KABYLE, TRANSLATION_PROMPT
from rag.retriever import KabyleRetriever


class KabyleAgroAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model
        self.retriever = KabyleRetriever()

    def _build_context(self, query: str) -> str:
        docs = self.retriever.retrieve(query, n_results=5)
        if not docs:
            return ""
        context_parts = ["Isallen n umawal d corpus (contexte RAG):"]
        for doc in docs:
            context_parts.append(f"- {doc['content']}")
        return "\n".join(context_parts)

    def chat(self, message: str, history: list[dict]) -> str:
        context = self._build_context(message)
        system = SYSTEM_PROMPT_KABYLE
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

    def stream_chat(self, message: str, history: list[dict]) -> AsyncGenerator:
        context = self._build_context(message)
        system = SYSTEM_PROMPT_KABYLE
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
            prompt = f"Traduis ce texte français en kabyle (avec translittération latine):\n\n{text}"
        else:
            prompt = f"Traduis ce texte kabyle en français:\n\n{text}"

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
