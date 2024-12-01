# app/retrieval/rag_engine.py

from typing import List, Dict, Any, Optional
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import logging

from ..config import get_settings
from ..database import VectorStore
from ..models import Message, MessageType
from .context import ContextManager

logger = logging.getLogger(__name__)
settings = get_settings()

class RAGEngine:
    """Retrieval Augmented Generation Engine"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.context_manager = ContextManager()
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.MAX_TOKENS
        )
        
        # Initialize prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", settings.SYSTEM_PROMPT),
            ("system", "Context information is below:\n{context}"),
            ("human", "{question}")
        ])

    async def get_response(
        self,
        question: str,
        conversation_history: Optional[List[Message]] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get response using RAG
        Args:
            question: User's question
            conversation_history: Previous messages in conversation
            user_id: User ID for context scoping
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Get relevant context
            context = await self.vector_store.get_relevant_context(
                query=question,
                max_chunks=settings.MAX_CONTEXT_CHUNKS,
                namespace=user_id
            )
            
            # Prepare conversation history if available
            history_context = ""
            if conversation_history:
                history_context = self.context_manager.format_conversation_history(
                    conversation_history
                )
                context = f"{history_context}\n\n{context}"
            
            # Generate response
            chain = self.prompt | self.llm
            response = await chain.ainvoke({
                "context": context,
                "question": question
            })
            
            return {
                "response": response.content,
                "context_used": context,
                "model_used": settings.OPENAI_MODEL,
                "conversation_history": history_context
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise