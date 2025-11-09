# main.py (refactored version)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from mistral_helper import MistralClient, MistralClientError


app = FastAPI(title="Mistral Chat Service", version="1.0.0")

# Global client instance reused across requests
client = MistralClient(log_prompts=False)


class ChatRequest(BaseModel):
    prompt: str = Field(..., description="The user message to send to the model.")
    system_prompt: str | None = Field(
        default=None,
        description="Optional system prompt to steer model behavior.",
    )
    temperature: float = Field(
        default=0.7, ge=0.0, le=2.0, description="Sampling temperature."
    )
    max_tokens: int = Field(
        default=512, gt=0, le=4096, description="Maximum number of tokens to generate."
    )
    safe_mode: bool = Field(
        default=True,
        description="Whether to enable safety filters, if supported.",
    )


class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Synchronous endpoint calling Mistral via our wrapper client.

    If you want an async version later, you'd:
    - make the route `async def`
    - use an async Mistral client method (`complete_async`)
    """
    try:
        answer = client.ask(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            safe_mode=request.safe_mode,
        )
        return ChatResponse(answer=answer)

    except MistralClientError as e:
        # Internal Mistral error: return 500, but don't leak internals
        # In real services you would log `e` and maybe `e.request_payload`
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Upstream model error. Please try again later.",
        ) from e


@app.get("/health")
def health_check() -> dict:
    """
    Simple health endpoint to check the service is up.
    """
    return {"status": "ok"}
