"""Mammouth AI clock rendering provider."""
from __future__ import annotations

from typing import List, Optional

from openai import OpenAI


class MammouthClockProvider:
    """Small helper around the OpenAI client configured for Mammouth."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        system_prompt: str,
        clock_prompt_template: str,
        temperature: float = 0.35,
        top_p: float = 0.9,
        max_output_tokens: int = 800,
    ) -> None:
        if not api_key:
            raise ValueError("Mammouth API key is required")

        self._api_key = api_key
        self._base_url = base_url
        self._system_prompt = system_prompt
        self._clock_prompt_template = clock_prompt_template
        self._temperature = temperature
        self._top_p = top_p
        self._max_output_tokens = max_output_tokens
        self._client: Optional[OpenAI] = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            self._client = OpenAI(api_key=self._api_key, base_url=self._base_url)
        return self._client

    def render_clock(
        self,
        model_id: str,
        *,
        current_time: Optional[str] = None,
        prompt_template: Optional[str] = None,
    ) -> str:
        template = prompt_template or self._clock_prompt_template
        clock_prompt = template.format(current_time=(current_time or "HH:MM:SS"))
        response = self.client.responses.create(
            model=model_id,
            temperature=self._temperature,
            top_p=self._top_p,
            max_output_tokens=self._max_output_tokens,
            stream=False,
            input=[
                {"role": "system", "content": [{"type": "text", "text": self._system_prompt}]},
                {"role": "user", "content": [{"type": "text", "text": clock_prompt}]},
            ],
        )
        html = self._extract_clock_markup(response)
        if not html:
            raise RuntimeError("Model response did not contain any renderable HTML.")
        return html

    @staticmethod
    def _extract_clock_markup(response) -> str:
        chunks: List[str] = []
        output = getattr(response, "output", [])
        for item in output or []:
            for content in getattr(item, "content", []) or []:
                if getattr(content, "type", None) == "output_text":
                    chunks.append(content.text)
        if chunks:
            return "".join(chunks).strip()
        fallback = getattr(response, "output_text", "")
        return str(fallback).strip()
