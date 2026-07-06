"""
Message service.

Responsible for message persistence.
"""

from sqlalchemy.orm import Session

from app.crud.message import (
    create_message,
    get_messages,
)
from app.models.message import Message
from app.models.conversation import Conversation


class MessageService:
    """
    Business logic for messages.
    """

    def create(
        self,
        db: Session,
        conversation: Conversation,
        role: str,
        content: str,
    ) -> Message:
        """
        Store a message.
        """

        message = Message(
            conversation_id=conversation.id,
            role=role,
            content=content,
        )

        return create_message(
            db,
            message,
        )

    def history(
        self,
        db: Session,
        conversation: Conversation,
    ) -> list[Message]:
        """
        Return conversation history.
        """

        return get_messages(
            db,
            conversation.id,
        )


message_service = MessageService()