from fastapi import APIRouter

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


@router.get("/")
def rag():
    return {
        "message": "RAG endpoint working"
    }