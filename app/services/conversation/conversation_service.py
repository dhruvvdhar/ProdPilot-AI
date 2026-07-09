"""
Conversation service.

Responsible for conversation lifecycle management.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.crud.conversation import (
    create_conversation,
    delete_conversation,
    get_conversation,
    get_user_conversations,
    rename_conversation
)
from app.models.conversation import Conversation
from app.models.user import User


class ConversationService:
    """
    Business logic for conversations.
    """

    def create(
        self,
        db: Session,
        current_user: User,
        title: str | None = None,
    ) -> Conversation:
        """
        Create a new conversation.
        """

        conversation = Conversation(
            title=title or "New Conversation",
            user_id=current_user.id,
        )

        return create_conversation(
            db,
            conversation,
        )

    def get(
        self,
        db: Session,
        conversation_id: int,
        current_user: User,
    ) -> Conversation | None:
        """
        Retrieve one conversation.
        """

        return get_conversation(
            db,
            conversation_id,
            current_user.id,
        )

    def list(
        self,
        db: Session,
        current_user: User,
    ) -> list[Conversation]:
        """
        Retrieve all conversations.
        """

        return get_user_conversations(
            db,
            current_user.id,
        )

    def delete(
        self,
        db: Session,
        conversation: Conversation,
    ) -> None:
        """
        Delete conversation.
        """

        delete_conversation(
            db,
            conversation,
        )

    def rename(
        self,
        db: Session,
        conversation: Conversation,
        title: str,
    ) -> Conversation:
        """
        Rename a conversation.
        """

        title = title.strip()

        if not title:
            raise ValueError("Title cannot be empty.")

        return rename_conversation(
            db,
            conversation,
            title,
        )
    

    def touch(
        self,
        db: Session,
        conversation: Conversation,
    ) -> None:
        """
        Update last activity timestamp.
        """

        conversation.updated_at = datetime.now(
            timezone.utc
        )

        db.commit()

        db.refresh(conversation)


conversation_service = ConversationService()