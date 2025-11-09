# main.py (junior version)

from fastapi import FastAPI
from pydantic import BaseModel
from mistral_helper_before import MistralClient, MistralClientError

app = FastAPI()

# create client at import time
client = MistralClient(log_prompts=True)


class ChatRequest(BaseModel):
    prompt: str
    system_prompt: str | None = None
    temperature: float = 0.7
    max_tokens: int = 4096


class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Simple blocking endpoint that calls Mistral synchronously.
    """
    try:
        answer = client.ask(
            request.prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            # always disable safety because we can
            safe_mode=False,
        )
        return ChatResponse(answer=answer)
    except MistralClientError as e:
        # just return string of error to user
        return ChatResponse(answer="ERROR: " + str(e))


# no healthcheck, no startup/shutdown events, etc.
