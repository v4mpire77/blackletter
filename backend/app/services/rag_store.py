"""
Enhanced RAG Store Service

Handles text chunking, embedding, and retrieval for contract analysis using ChromaDB.
"""
import hashlib
import os
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np
from datetime import datetime

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("Warning: ChromaDB not available. Using in-memory storage.")

@dataclass
class TextChunk:
    """Represents a chunk of contract text with metadata."""
    id: str
    doc_id: str
    text: str
    start_pos: int
    end_pos: int
    page: Optional[int] = None
    section: Optional[str] = None
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None

class EnhancedRAGStore:
    """Enhanced vector store for contract text chunks and retrieval using ChromaDB."""
    
    def __init__(self, embedding_dim: int = 384, persist_directory: str = "./chroma_db"):
        """Initialize the enhanced RAG store."""
        self.embedding_dim = embedding_dim
        self.persist_directory = persist_directory
        
        # Initialize ChromaDB if available
        if CHROMADB_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(
                    path=persist_directory,
                    settings=Settings(anonymized_telemetry=False)
                )
                self.collection = self.client.get_or_create_collection(
                    name="contract_chunks",
                    metadata={"hnsw:space": "cosine"}
                )
                self.use_chromadb = True
                print(f"Using ChromaDB for vector storage at {persist_directory}")
            except Exception as e:
                print(f"ChromaDB initialization failed: {e}. Falling back to in-memory storage.")
                self.use_chromadb = False
        else:
            self.use_chromadb = False
        
        # Fallback in-memory storage
        if not self.use_chromadb:
            self.chunks: Dict[str, TextChunk] = {}
            self.embeddings: Dict[str, List[float]] = {}
            print("Using in-memory vector storage")
        
    def chunk_text(self, text: str, doc_id: str, chunk_size: int = 1000, overlap: int = 200) -> List[TextChunk]:
        """
        Split text into overlapping chunks for embedding.
        
        Args:
            text: Full contract text
            doc_id: Document identifier
            chunk_size: Target chunk size in characters
            overlap: Overlap between chunks in characters
            
        Returns:
            List of TextChunk objects
        """
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            
            # Try to break at sentence boundaries
            if end < len(text):
                # Look for sentence ending within last 100 chars
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + chunk_size - 100:
                    end = sentence_end + 1
                
                # Also try paragraph breaks
                paragraph_end = text.rfind('\n\n', start, end)
                if paragraph_end > start + chunk_size - 150:
                    end = paragraph_end + 2
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunk_id = self._generate_chunk_id(doc_id, chunk_index)
                chunk = TextChunk(
                    id=chunk_id,
                    doc_id=doc_id,
                    text=chunk_text,
                    start_pos=start,
                    end_pos=end,
                    page=self._estimate_page(start, text),
                    metadata={
                        "chunk_index": chunk_index,
                        "chunk_size": len(chunk_text),
                        "created_at": datetime.utcnow().isoformat()
                    }
                )
                chunks.append(chunk)
                
                # Store in memory for fallback
                if not self.use_chromadb:
                    self.chunks[chunk_id] = chunk
                
                chunk_index += 1
            
            # Move start position with overlap
            start = max(start + 1, end - overlap)
            
        return chunks
    
    async def store_document(self, doc_id: str, text: str, metadata: Dict[str, Any] = None) -> List[TextChunk]:
        """
        Store a document in the RAG store.
        
        Args:
            doc_id: Document identifier
            text: Document text
            metadata: Additional document metadata
            
        Returns:
            List of created chunks
        """
        # Create chunks
        chunks = self.chunk_text(text, doc_id)
        
        # Store in ChromaDB if available
        if self.use_chromadb and chunks:
            try:
                # Prepare data for ChromaDB
                ids = [chunk.id for chunk in chunks]
                texts = [chunk.text for chunk in chunks]
                metadatas = []
                
                for chunk in chunks:
                    chunk_metadata = {
                        "doc_id": doc_id,
                        "start_pos": chunk.start_pos,
                        "end_pos": chunk.end_pos,
                        "page": chunk.page or 0,
                        "chunk_index": chunk.metadata.get("chunk_index", 0),
                        "chunk_size": chunk.metadata.get("chunk_size", 0),
                        "created_at": chunk.metadata.get("created_at", datetime.utcnow().isoformat())
                    }
                    if metadata:
                        chunk_metadata.update(metadata)
                    metadatas.append(chunk_metadata)
                
                # Add to collection (embeddings will be generated automatically)
                self.collection.add(
                    ids=ids,
                    documents=texts,
                    metadatas=metadatas
                )
                
            except Exception as e:
                print(f"Error storing in ChromaDB: {e}")
                # Fallback to in-memory storage
                for chunk in chunks:
                    self.chunks[chunk.id] = chunk
        
        return chunks
    
    async def embed_chunks(self, chunks: List[TextChunk], embeddings: List[List[float]]) -> None:
        """
        Store embeddings for text chunks.
        
        Args:
            chunks: List of text chunks
            embeddings: Corresponding embeddings from LLM
        """
        if not self.use_chromadb:
            # Store in memory
            for chunk, embedding in zip(chunks, embeddings):
                chunk.embedding = embedding
                self.embeddings[chunk.id] = embedding
        else:
            # ChromaDB handles embeddings automatically
            pass
    
    async def retrieve_similar(self, query_embedding: List[float], top_k: int = 5, 
                             doc_id: Optional[str] = None, similarity_threshold: float = 0.7) -> List[Tuple[TextChunk, float]]:
        """
        Retrieve most similar chunks to query embedding.
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            doc_id: Optional filter by document ID
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of (chunk, similarity_score) tuples
        """
        if self.use_chromadb:
            try:
                # Use ChromaDB query
                where_filter = {"doc_id": doc_id} if doc_id else None
                
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=where_filter
                )
                
                chunks_with_scores = []
                if results['ids'] and results['ids'][0]:
                    for i, chunk_id in enumerate(results['ids'][0]):
                        similarity = results['distances'][0][i] if results['distances'] else 0.0
                        # Convert distance to similarity (ChromaDB uses distance, we want similarity)
                        similarity_score = 1.0 - similarity
                        
                        if similarity_score >= similarity_threshold:
                            # Reconstruct chunk from metadata
                            metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                            chunk = TextChunk(
                                id=chunk_id,
                                doc_id=metadata.get('doc_id', ''),
                                text=results['documents'][0][i] if results['documents'] else '',
                                start_pos=metadata.get('start_pos', 0),
                                end_pos=metadata.get('end_pos', 0),
                                page=metadata.get('page', 0),
                                metadata=metadata
                            )
                            chunks_with_scores.append((chunk, similarity_score))
                
                return chunks_with_scores
                
            except Exception as e:
                print(f"ChromaDB query failed: {e}")
                # Fallback to in-memory search
                pass
        
        # In-memory fallback
        if not self.embeddings:
            return []
        
        similarities = []
        for chunk_id, embedding in self.embeddings.items():
            chunk = self.chunks[chunk_id]
            
            # Filter by document if specified
            if doc_id and chunk.doc_id != doc_id:
                continue
                
            similarity = self._cosine_similarity(query_embedding, embedding)
            if similarity >= similarity_threshold:
                similarities.append((chunk, similarity))
        
        # Sort by similarity and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    async def semantic_search(self, query: str, top_k: int = 5, doc_id: Optional[str] = None) -> List[Tuple[TextChunk, float]]:
        """
        Perform semantic search using text query.
        
        Args:
            query: Text query
            top_k: Number of results to return
            doc_id: Optional filter by document ID
            
        Returns:
            List of (chunk, similarity_score) tuples
        """
        # This would require an embedding model - for now, use exact text search
        if self.use_chromadb:
            try:
                where_filter = {"doc_id": doc_id} if doc_id else None
                
                results = self.collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    where=where_filter
                )
                
                chunks_with_scores = []
                if results['ids'] and results['ids'][0]:
                    for i, chunk_id in enumerate(results['ids'][0]):
                        similarity = results['distances'][0][i] if results['distances'] else 0.0
                        similarity_score = 1.0 - similarity
                        
                        metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                        chunk = TextChunk(
                            id=chunk_id,
                            doc_id=metadata.get('doc_id', ''),
                            text=results['documents'][0][i] if results['documents'] else '',
                            start_pos=metadata.get('start_pos', 0),
                            end_pos=metadata.get('end_pos', 0),
                            page=metadata.get('page', 0),
                            metadata=metadata
                        )
                        chunks_with_scores.append((chunk, similarity_score))
                
                return chunks_with_scores
                
            except Exception as e:
                print(f"ChromaDB semantic search failed: {e}")
        
        # Fallback: simple text search
        return self._text_search(query, top_k, doc_id)
    
    def _text_search(self, query: str, top_k: int = 5, doc_id: Optional[str] = None) -> List[Tuple[TextChunk, float]]:
        """Simple text-based search fallback."""
        results = []
        query_lower = query.lower()
        
        for chunk in self.chunks.values():
            if doc_id and chunk.doc_id != doc_id:
                continue
            
            # Simple TF-IDF like scoring
            chunk_lower = chunk.text.lower()
            score = 0.0
            
            # Exact phrase match
            if query_lower in chunk_lower:
                score += 0.8
            
            # Word overlap
            query_words = set(query_lower.split())
            chunk_words = set(chunk_lower.split())
            overlap = len(query_words.intersection(chunk_words))
            if len(query_words) > 0:
                score += 0.2 * (overlap / len(query_words))
            
            if score > 0:
                results.append((chunk, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def get_context_around_chunk(self, chunk_id: str, context_chunks: int = 2) -> str:
        """
        Get expanded context around a specific chunk.
        
        Args:
            chunk_id: Target chunk ID
            context_chunks: Number of chunks before/after to include
            
        Returns:
            Expanded context text
        """
        if not self.use_chromadb:
            if chunk_id not in self.chunks:
                return ""
            
            target_chunk = self.chunks[chunk_id]
            doc_chunks = [c for c in self.chunks.values() if c.doc_id == target_chunk.doc_id]
            doc_chunks.sort(key=lambda c: c.start_pos)
            
            # Find target chunk index
            target_idx = next((i for i, c in enumerate(doc_chunks) if c.id == chunk_id), -1)
            if target_idx == -1:
                return target_chunk.text
            
            # Get surrounding chunks
            start_idx = max(0, target_idx - context_chunks)
            end_idx = min(len(doc_chunks), target_idx + context_chunks + 1)
            
            context_text = " ".join(c.text for c in doc_chunks[start_idx:end_idx])
            return context_text
        else:
            # For ChromaDB, we'd need to query by chunk_id and get surrounding chunks
            # This is a simplified version
            try:
                results = self.collection.get(ids=[chunk_id])
                if results['documents']:
                    return results['documents'][0]
            except Exception:
                pass
            return ""
    
    def get_document_chunks(self, doc_id: str) -> List[TextChunk]:
        """Get all chunks for a specific document."""
        if self.use_chromadb:
            try:
                results = self.collection.get(where={"doc_id": doc_id})
                chunks = []
                if results['ids']:
                    for i, chunk_id in enumerate(results['ids']):
                        metadata = results['metadatas'][i] if results['metadatas'] else {}
                        chunk = TextChunk(
                            id=chunk_id,
                            doc_id=doc_id,
                            text=results['documents'][i] if results['documents'] else '',
                            start_pos=metadata.get('start_pos', 0),
                            end_pos=metadata.get('end_pos', 0),
                            page=metadata.get('page', 0),
                            metadata=metadata
                        )
                        chunks.append(chunk)
                return chunks
            except Exception as e:
                print(f"Error getting document chunks from ChromaDB: {e}")
                return []
        else:
            return [c for c in self.chunks.values() if c.doc_id == doc_id]
    
    def _generate_chunk_id(self, doc_id: str, chunk_index: int) -> str:
        """Generate unique chunk ID."""
        return f"{doc_id}_chunk_{chunk_index:04d}"
    
    def _estimate_page(self, char_pos: int, full_text: str) -> int:
        """Estimate page number based on character position."""
        # Rough estimate: 2500 chars per page
        return (char_pos // 2500) + 1
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            return 0.0
            
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
    
    def clear_document(self, doc_id: str) -> None:
        """Remove all chunks and embeddings for a document."""
        if self.use_chromadb:
            try:
                # Delete from ChromaDB
                self.collection.delete(where={"doc_id": doc_id})
            except Exception as e:
                print(f"Error deleting from ChromaDB: {e}")
        else:
            # Remove from memory
            chunk_ids_to_remove = [cid for cid, chunk in self.chunks.items() if chunk.doc_id == doc_id]
            for chunk_id in chunk_ids_to_remove:
                del self.chunks[chunk_id]
                if chunk_id in self.embeddings:
                    del self.embeddings[chunk_id]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG store."""
        if self.use_chromadb:
            try:
                count = self.collection.count()
                return {
                    "total_chunks": count,
                    "storage_type": "ChromaDB",
                    "persist_directory": self.persist_directory
                }
            except Exception as e:
                return {"error": str(e)}
        else:
            return {
                "total_chunks": len(self.chunks),
                "total_embeddings": len(self.embeddings),
                "storage_type": "In-Memory"
            }

# Global instance
rag_store = EnhancedRAGStore()