# ProdPilot AI — Frontend (V2)

React + TypeScript + Vite + Tailwind CSS frontend for the ProdPilot AI backend. Fully wired
to the real FastAPI API — no mock/dummy data.

## Stack

- **React 19 + TypeScript** — UI
- **Vite** — dev server & build
- **Tailwind CSS v4** — styling, brand tokens derived from the logo (blue -> teal)
- **React Router** — routing / auth guards
- **TanStack Query** — server state, caching, polling
- **Axios** — HTTP client with JWT interceptor
- **react-hot-toast** — notifications
- **react-markdown** — renders assistant answers (supports lists, code blocks, etc.)
- **lucide-react** — icons

## Getting started

```bash
cd frontend
npm install
npm run dev
```

The app runs at `http://localhost:5173` (the backend's CORS config already allows this
origin — see `app/main.py`).

Set the backend URL in `.env` (already created, copy `.env.example` if you re-clone):

```
VITE_API_BASE_URL=http://localhost:8000
```

Make sure the backend is running (`python -m uvicorn app.main:app --reload`) with your
`.env` (`GROQ_API_KEY`, `DATABASE_URL`, `SECRET_KEY`) configured, and that migrations have
been applied (`alembic upgrade head`).

## Project structure

```
src/
  api/            # One file per backend resource - axios calls only, no UI logic
  components/
    auth/         # Auth page layout
    chat/         # Conversation list, chat window, message bubble, input
    documents/    # Uploader + document table row
    layout/       # App shell (sidebar/nav)
    ui/           # Generic primitives (Button, Input, Badge, Spinner, ConfirmDialog)
  context/        # AuthContext (session bootstrap, login/register/logout)
  hooks/          # TanStack Query hooks per resource (useChat, useDocuments, ...)
  pages/          # Route-level screens
  routes/         # ProtectedRoute / GuestRoute guards
  types/          # TypeScript types mirrored 1:1 from the backend Pydantic schemas
```

This separation (api -> hooks -> components -> pages) keeps each layer swappable - e.g. you
can add a new resource by adding one `api/*.ts` file and one `hooks/use*.ts` file without
touching existing code, or swap TanStack Query for something else later without touching
components.

## Backend endpoints used

| Feature | Method & path |
|---|---|
| Register | `POST /auth/register` |
| Login | `POST /auth/login` |
| Current user | `GET /auth/me` |
| List conversations | `GET /conversations` |
| Create conversation | `POST /conversations` |
| Delete conversation | `DELETE /conversations/{id}` |
| Conversation messages | `GET /conversations/{id}/messages` |
| Chat (streaming) | `POST /chat/stream` |
| Chat (non-streaming, available but unused by UI) | `POST /chat/` |
| List documents | `GET /documents/` |
| Upload document | `POST /documents/upload` |
| Delete document | `DELETE /documents/{id}` |

## Backend additions made to support this frontend

Two small, additive, non-breaking changes were made to the backend so nothing in the UI
relies on placeholder data:

1. **`GET /conversations/{id}/messages`** (`app/api/v1/conversations.py`) - new endpoint
   that reuses the existing `get_messages_by_conversation` CRUD function so the chat UI can
   restore a conversation's history when reopened.
2. **`DocumentResponse` schema** (`app/schemas/document.py`) - now also returns the
   `parse_status`, `embedding_status`, `vectorstore_status`, `chunk_count`, `vector_count`,
   and `error_message` columns that already existed on the `Document` model, so the
   Documents page can show real ingestion pipeline progress instead of guessing.

No existing endpoint behavior, request shape, or response field was changed or removed.

## Known limitation (by design, per current scope)

"Report a bug" is present in the sidebar but disabled with a tooltip, since there's no
backend table/endpoint for it yet - exactly as scoped for this pass.

## Scaling this further

- Add a resource: create `api/<resource>.ts` + `hooks/use<Resource>.ts`, following the
  pattern used by `documents`/`conversations`.
- Swap the streaming transport: `api/chat.ts` isolates all SSE-parsing logic in
  `streamChat()`, so switching to WebSockets later only touches that one file.
- Theming: brand colors are CSS variables in `src/index.css` (`@theme` block) - update
  them there to restyle the whole app.
