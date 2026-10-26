# API Contract - Customer Support Chatbot (v1)

Backend and frontend both build against this document. Change it only through a pull request that both roles review.

- Local base URL: `http://127.0.0.1:8000`
- All requests and responses are JSON (`Content-Type: application/json`).

## GET /health

Checks that the server is running. Does not call Groq.

- Success `200`: `{"status": "ok"}`

## POST /chat

Sends one customer message and returns one reply. Each request is independent: v1 has no conversation memory.

Request body:

| Field | Type | Rules |
|-------|------|-------|
| `message` | string | required; after trimming spaces, 1 to 1000 characters |

Example request: `{"message": "What are your business hours?"}`

Success `200`: `{"reply": "<text>"}`

- `reply` is always a non-empty string.
- Illustrative example only, not an implemented feature: `{"reply": "We are open Monday to Friday, 9 AM to 6 PM."}`

## Errors

Every error response has the same shape: `{"detail": "<human-readable message>"}`

| Status | When | Example `detail` |
|--------|------|------------------|
| 422 | `message` missing, not a string, empty or whitespace only, or over 1000 characters | `Message must be between 1 and 1000 characters.` |
| 429 | Too many requests (Groq rate limit or our own limit) | `Too many requests. Please wait a moment and try again.` |
| 502 | The AI provider failed or could not be reached | `The assistant is temporarily unavailable. Please try again.` |
| 500 | Unexpected server error, including missing configuration | `Something went wrong on our side.` |

Rules:
- `detail` never contains API keys, stack traces or raw provider errors.
- The frontend shows `detail` to the user as it is.
- The backend is the source of truth for validation. The frontend also limits input to 1000 characters for a better user experience.

## CORS

The backend allows browser requests from the local frontend origins `http://127.0.0.1:5500` and `http://localhost:5500`. These are different origins, so both are listed.

## Not in v1

Order lookups, refunds, account-specific actions, conversation history, authentication.