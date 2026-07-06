"""
Conversation memory service.
"""

from sqlalchemy.orm import Session

from app.crud.message import get_messages_by_conversation


class MemoryService:
    """
    Builds formatted conversation history
    from stored chat messages.
    """

    def build_history(
        self,
        db: Session,
        conversation_id: int,
    ) -> str:

        messages = get_messages_by_conversation(
            db,
            conversation_id,
        )

        if not messages:
            return ""

        history = []

        for message in messages:

            role = (
                "User"
                if message.role == "user"
                else "Assistant"
            )

            history.append(
                f"{role}: {message.content}"
            )

        return "\n".join(history)


memory_service = MemoryService()