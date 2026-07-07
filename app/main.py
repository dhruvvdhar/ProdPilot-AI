from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.observability import enable_tracing

from app.api.v1.auth import router as auth_router
from app.api.v1.chat import router as chat_router
from app.api.v1.documents import router as documents_router
from app.api.v1.rag import router as rag_router
from app.api.v1 import documents
from app.api.v1.conversations import (
    router as conversations_router,
)

from app.core.exceptions import ProdPilotException
from app.core.exception_handlers import (
    prodpilot_exception_handler,
    generic_exception_handler,
    http_exception_handler,
)

from app.services.hybrid_search.bm25_service import (
    bm25_service,
)

tracer = enable_tracing()
tracer.__enter__()

app = FastAPI(
    title="ProdPilot AI",
    version="2.0.0",
    description="AI Powered Production Support Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bm25_service.load_index()

app.add_exception_handler(
    ProdPilotException,
    prodpilot_exception_handler,
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(rag_router)
app.include_router(documents.router)
app.include_router(conversations_router)


@app.get("/")
def root():
    return {
        "application": "ProdPilot AI",
        "version": "2.0.0",
        "status": "Running",
    }