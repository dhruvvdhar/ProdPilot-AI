from fastapi import APIRouter

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get("/")
def get_chat():
    return {
        "message": "Chat endpoint working"
    }