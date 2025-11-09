# mistral_helper_before.py (junior version)

import os
from mistralai import Mistral


DEFAULT_MODEL = "mistral-tiny-latest"
API_KEY_ENV = "MISTRAL_API_KEY"


class MistralClientError(Exception):
    """Error when talking to Mistral API."""
    pass


class MistralClient:
    def __init__(self, api_key=None, model=DEFAULT_MODEL, log_prompts=False):
        self.api_key = api_key or os.getenv(API_KEY_ENV)
        if not self.api_key:
            # just hope caller sees this
            print("No API key found!")
        self.model = model
        self.log_prompts = log_prompts
        # client may be created even if api_key is missing
        self.client = Mistral(api_key=self.api_key)

    def build_messages(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages

    def ask(
        self,
        prompt,
        system_prompt=None,
        temperature=0.7,
        max_tokens=4096,
        safe_mode=False,
    ):
        messages = self.build_messages(prompt, system_prompt)

        if self.log_prompts:
            # log everything, including full user content
            print("[MistralClient] Sending messages:", messages)

        try:
            resp = self.client.chat.complete(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                safe_mode=safe_mode,
            )
        except Exception as e:
            # lose original traceback and context
            raise MistralClientError("Mistral call failed: " + str(e))

        # assume dict-like message
        return resp.choices[0].message["content"]

