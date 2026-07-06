"""
CRUD operations for conversations.
"""

from sqlalchemy.orm import Session

from app.models.conversation import Conversation


def create_conversation(
    db: Session,
    conversation: Conversation,
) -> Conversation:
    """
    Persist a conversation.
    """

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
) -> Conversation | None:
    """
    Retrieve a user's conversation.
    """

    return (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )


def get_user_conversations(
    db: Session,
    user_id: int,
) -> list[Conversation]:
    """
    Retrieve every conversation belonging
    to a user.
    """

    return (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id
        )
        .order_by(
            Conversation.updated_at.desc()
        )
        .all()
    )


def delete_conversation(
    db: Session,
    conversation: Conversation,
) -> None:
    """
    Delete a conversation.
    """

    db.delete(conversation)
    db.commit()