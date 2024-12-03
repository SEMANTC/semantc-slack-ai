# app/database/vector_store.

from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone as PineconeClient
from typing import List, Dict, Any, Optional
import logging

from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class VectorStore:
    def __init__(self):
        """Initialize vector store with Pinecone"""
        try:
            # Initialize embeddings
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-large",
                openai_api_key=settings.OPENAI_API_KEY
            )
            
            # Initialize Pinecone
            self.pc = PineconeClient(api_key=settings.PINECONE_API_KEY)
            self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
            
            # Initialize vector store
            self.vector_store = PineconeVectorStore(
                index=self.index,
                embedding=self.embeddings,
                text_key="text",
                namespace="default"
            )
            
            logger.info("Vector store initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")
            raise

    async def similarity_search(
        self, 
        query: str, 
        k: int = 3,
        threshold: float = 0.7,
        namespace: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        Args:
            query: Search query
            k: Number of results to return
            threshold: Similarity threshold
            namespace: Optional namespace for scoping results
        """
        try:
            results = await self.vector_store.asimilarity_search_with_score(
                query, 
                k=k,
                namespace=namespace
            )
            
            # Filter by threshold and format results
            filtered_results = [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score
                }
                for doc, score in results
                if score >= threshold
            ]
            
            return filtered_results
            
        except Exception as e:
            logger.error(f"Error during similarity search: {str(e)}")
            raise

    async def get_relevant_context(
        self, 
        query: str, 
        max_chunks: int = 5,
        namespace: Optional[str] = None
    ) -> str:
        """
        Get relevant context for a query
        Args:
            query: Search query
            max_chunks: Maximum number of chunks to return
            namespace: Optional namespace for scoping results
        """
        try:
            results = await self.similarity_search(
                query,
                k=max_chunks,
                namespace=namespace
            )
            
            if not results:
                return ""
            
            # Concatenate contexts with metadata
            contexts = []
            for result in results:
                content = result["content"]
                metadata = result["metadata"]
                source = metadata.get("source", "Unknown")
                contexts.append(f"Source: {source}\nContent: {content}\n")
            
            return "\n".join(contexts)
            
        except Exception as e:
            logger.error(f"Error getting relevant context: {str(e)}")
            return ""