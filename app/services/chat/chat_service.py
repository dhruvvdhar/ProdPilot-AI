"""
Chat orchestration service.
"""

from sqlalchemy.orm import Session
from app.crud.conversation import get_conversation
from app.crud.message import create_message
from app.models.message import Message
from app.models.user import User
from app.services.memory.memory_service import memory_service
from app.services.rag.rag_service import RAGService
from app.core.exceptions import ConversationNotFoundException
from app.services.citations.citation_service import citation_service
from app.services.guardrails import guardrail_service

class ChatService:
    """
    Orchestrates the conversational RAG pipeline.
    """

    def __init__(self):

        self._rag = RAGService()

    def chat(
        self,
        db: Session,
        conversation_id: int,
        question: str,
        current_user: User,
    ) :
        guardrail_service.validate(question)
        conversation = get_conversation(
            db,
            conversation_id,
            current_user.id,
        )

        if conversation is None:
            raise ConversationNotFoundException(
                "Conversation not found."
            )

        create_message(
            db,
            Message(
                conversation_id=conversation_id,
                role="user",
                content=question,
            ),
        )

        history = memory_service.build_history(
            db,
            conversation_id,
        )

        rag_response = self._rag.ask(
            question=question,
            history=history,
        )

        answer = rag_response["answer"]
        documents = rag_response["documents"]
        citations = citation_service.build(
            documents
        )

        create_message(
            db,
            Message(
                conversation_id=conversation_id,
                role="assistant",
                content=answer,
            ),
        )

        return {
            "answer": answer,
            "citations": citations,
        }
    
    def stream_chat(
        self,
        db: Session,
        conversation_id: int,
        question: str,
        current_user: User,
    ):

        guardrail_service.validate(question)

        conversation = get_conversation(
            db,
            conversation_id,
            current_user.id,
        )

        if conversation is None:
            raise ConversationNotFoundException(
                "Conversation not found."
            )

        create_message(
            db,

        Message(
            conversation_id=conversation_id,
            role="user",
            content=question,
        ),
    )

        history = memory_service.build_history(
            db,
            conversation_id,
        )

        assistant_answer = ""

        documents = []

        for event in self._rag.stream(
            question=question,
            history=history,
        ):

            if event["type"] == "token":

                assistant_answer += event["data"]

                yield {
                    "type": "token",
                    "data": event["data"],
                }

            elif event["type"] == "documents":

                documents = event["data"]

        citations = citation_service.build(
            documents
        )

        yield {
            "type": "citations",
            "data": [
                citation.model_dump()
                for citation in citations
            ],
        }

        create_message(
            db,
            Message(
                conversation_id=conversation_id,
                role="assistant",
                content=assistant_answer,
            ),
        )
        


chat_service = ChatService()