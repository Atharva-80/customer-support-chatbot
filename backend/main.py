"""Customer Support Chatbot - FastAPI backend.

Milestone 3: placeholder replies only. Groq is connected in the next milestone.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator

MAX_MESSAGE_LENGTH = 1000
ALLOWED_ORIGINS = ["http://127.0.0.1:5500", "http://localhost:5500"]

app = FastAPI(title="Customer Support Chatbot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def check_message(cls, value: str) -> str:
        value = value.strip()
        if not 1 <= len(value) <= MAX_MESSAGE_LENGTH:
            raise ValueError("message length out of range")
        return value


class ChatResponse(BaseModel):
    reply: str


@app.exception_handler(RequestValidationError)
async def handle_invalid_request(request: Request, exc: RequestValidationError) -> JSONResponse:
    # The API contract promises one error shape: {"detail": "<message>"}
    return JSONResponse(
        status_code=422,
        content={"detail": f"Message must be between 1 and {MAX_MESSAGE_LENGTH} characters."},
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    # Placeholder only. A real Groq call replaces this in Milestone 4.
    return ChatResponse(reply=f"[placeholder reply, Groq not connected yet] You said: {body.message}")