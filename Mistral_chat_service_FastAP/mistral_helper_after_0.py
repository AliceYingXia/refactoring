# mistral_helper.py (refactored version)

import os
from typing import List, Dict, Optional

from mistralai import Mistral


DEFAULT_MODEL = "mistral-tiny-latest"
API_KEY_ENV = "MISTRAL_API_KEY"


class MistralClientError(Exception):
    """
    High-level wrapper for errors when calling the Mistral API.
    """

    def __init__(
        self,
        message: str,
        *,
        original_exc: Optional[BaseException] = None,
        model: Optional[str] = None,
        request_payload: Optional[dict] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.original_exc = original_exc
        self.model = model
        self.request_payload = request_payload

    def __str__(self) -> str:
        base = self.message
        if self.model:
            base += f" [model={self.model}]"
        if self.original_exc is not None:
            base += f" (caused by {type(self.original_exc).__name__}: {self.original_exc})"
        return base


class MistralClient:
    """
    Simple sync wrapper for Mistral chat completion.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        log_prompts: bool = False,
    ) -> None:
        self.api_key = api_key or os.getenv(API_KEY_ENV)
        if not self.api_key:
            raise ValueError(
                f"Mistral API key not found. Pass `api_key` or set env {API_KEY_ENV}"
            )

        self.model = model
        self.log_prompts = log_prompts
        self._client = Mistral(api_key=self.api_key)

    def _build_messages(
        self,
        prompt: str,
        system_prompt: Optional[str],
    ) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages

    def ask(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        *,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        safe_mode: bool = True,
    ) -> str:
        messages = self._build_messages(prompt, system_prompt)

        if self.log_prompts:
            # Avoid logging full text in real production
            print(
                "[MistralClient] Sending chat completion request:",
                f"model={self.model}, num_messages={len(messages)}",
            )

        try:
            resp = self._client.chat.complete(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                safe_mode=safe_mode,
            )
        except Exception as exc:
            payload_meta = {
                "model": self.model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "safe_mode": safe_mode,
                "num_messages": len(messages),
            }
            raise MistralClientError(
                "Error calling Mistral chat completion",
                original_exc=exc,
                model=self.model,
                request_payload=payload_meta,
            ) from exc

        return resp.choices[0].message.content
