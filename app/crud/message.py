"""
CRUD operations for messages.
"""

from sqlalchemy.orm import Session

from app.models.message import Message


def create_message(
    db: Session,
    message: Message,
) -> Message:
    """
    Persist a message.
    """

    db.add(message)
    db.commit()
    db.refresh(message)

    return message

     


def get_messages_by_conversation(
    db: Session,
    conversation_id: int,
):

    return (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(Message.created_at.asc())
        .all()
    )