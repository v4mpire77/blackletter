"""
Vector database adapter for Blackletter Systems.

This module provides functionality for interacting with vector databases:
- Weaviate (default)
- Support for Qdrant can be added later

Usage:
    from app.core.vectors import get_vector_client, add_document, search_documents
    
    # Add a document to the vector database
    doc_id = await add_document(
        text="This is a legal document...",
        metadata={"source": "contract.pdf", "page": 1}
    )
    
    # Search for similar documents
    results = await search_documents("liability clause", limit=5)
"""

import os
import uuid
from typing import Dict, List, Optional, Tuple, Union, Any
import logging
import json
import hashlib

import weaviate
from weaviate.util import generate_uuid5

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment configuration
VECTOR_PROVIDER = os.getenv("VECTOR_PROVIDER", "weaviate").lower()
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8081")

# Schema definitions
DOCUMENT_CLASS_NAME = "Document"
DOCUMENT_SCHEMA = {
    "class": DOCUMENT_CLASS_NAME,
    "vectorizer": "text2vec-transformers",
    "properties": [
        {
            "name": "content",
            "dataType": ["text"],
            "description": "The document text content"
        },
        {
            "name": "source",
            "dataType": ["string"],
            "description": "Source identifier (e.g., filename, URL)"
        },
        {
            "name": "sourceType",
            "dataType": ["string"],
            "description": "Type of source (e.g., contract, legislation, case)"
        },
        {
            "name": "page",
            "dataType": ["int"],
            "description": "Page number in the source document"
        },
        {
            "name": "paragraph",
            "dataType": ["int"],
            "description": "Paragraph number in the source document"
        },
        {
            "name": "metadata",
            "dataType": ["text"],
            "description": "Additional metadata as JSON string"
        }
    ]
}

# Client instance
_vector_client = None

def get_vector_client():
    """
    Get or initialize the vector database client.
    
    Returns:
        object: The vector database client
    """
    global _vector_client
    if _vector_client is None:
        if VECTOR_PROVIDER == "weaviate":
            _vector_client = weaviate.Client(url=WEAVIATE_URL)
        else:
            raise ValueError(f"Unsupported vector provider: {VECTOR_PROVIDER}")
    return _vector_client

def ensure_schema_exists():
    """
    Ensure that the vector database schema exists, creating it if necessary.
    
    Returns:
        bool: True if the schema exists or was created
    """
    client = get_vector_client()
    
    try:
        # Check if the schema exists
        schema = client.schema.get()
        classes = [c["class"] for c in schema["classes"]] if "classes" in schema else []
        
        if DOCUMENT_CLASS_NAME not in classes:
            # Create the schema
            client.schema.create_class(DOCUMENT_SCHEMA)
            logger.info(f"Created schema for {DOCUMENT_CLASS_NAME}")
        else:
            logger.info(f"Schema for {DOCUMENT_CLASS_NAME} already exists")
        
        return True
    
    except Exception as e:
        logger.error(f"Error ensuring schema exists: {str(e)}")
        raise

async def add_document(
    text: str,
    source: Optional[str] = None,
    source_type: Optional[str] = None,
    page: Optional[int] = None,
    paragraph: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None,
    doc_id: Optional[str] = None
) -> str:
    """
    Add a document to the vector database.
    
    Args:
        text: The document text
        source: Source identifier (e.g., filename, URL)
        source_type: Type of source (e.g., contract, legislation, case)
        page: Page number in the source document
        paragraph: Paragraph number in the source document
        metadata: Additional metadata
        doc_id: Optional document ID (generated if not provided)
        
    Returns:
        str: The document ID
    """
    client = get_vector_client()
    ensure_schema_exists()
    
    # Generate a deterministic ID if not provided
    if not doc_id:
        # Create a unique ID based on content and source
        content_hash = hashlib.md5(text.encode()).hexdigest()
        source_str = str(source or "")
        doc_id = generate_uuid5(source_str + content_hash)
    
    # Prepare the document properties
    properties = {
        "content": text,
    }
    
    if source:
        properties["source"] = source
    
    if source_type:
        properties["sourceType"] = source_type
    
    if page is not None:
        properties["page"] = page
    
    if paragraph is not None:
        properties["paragraph"] = paragraph
    
    if metadata:
        properties["metadata"] = json.dumps(metadata)
    
    try:
        # Add the document to Weaviate
        client.data_object.create(
            data_object=properties,
            class_name=DOCUMENT_CLASS_NAME,
            uuid=doc_id
        )
        
        logger.info(f"Added document {doc_id} to vector database")
        return doc_id
    
    except Exception as e:
        logger.error(f"Error adding document to vector database: {str(e)}")
        raise

async def search_documents(
    query: str,
    limit: int = 10,
    source_type: Optional[str] = None,
    source: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search for documents similar to the query.
    
    Args:
        query: The search query
        limit: Maximum number of results to return
        source_type: Optional filter by source type
        source: Optional filter by source
        
    Returns:
        List[Dict[str, Any]]: List of matching documents
    """
    client = get_vector_client()
    
    try:
        # Build the query
        weaviate_query = client.query.get(
            DOCUMENT_CLASS_NAME,
            ["content", "source", "sourceType", "page", "paragraph", "metadata", "_additional {certainty}"]
        ).with_near_text({"concepts": [query]}).with_limit(limit)
        
        # Add filters if provided
        if source_type or source:
            filter_obj = {"operator": "And", "operands": []}
            
            if source_type:
                filter_obj["operands"].append({
                    "path": ["sourceType"],
                    "operator": "Equal",
                    "valueString": source_type
                })
            
            if source:
                filter_obj["operands"].append({
                    "path": ["source"],
                    "operator": "Equal",
                    "valueString": source
                })
            
            weaviate_query = weaviate_query.with_where(filter_obj)
        
        # Execute the query
        result = weaviate_query.do()
        
        # Process the results
        documents = []
        if "data" in result and "Get" in result["data"] and DOCUMENT_CLASS_NAME in result["data"]["Get"]:
            for item in result["data"]["Get"][DOCUMENT_CLASS_NAME]:
                doc = {
                    "id": item["_additional"]["id"],
                    "content": item["content"],
                    "score": item["_additional"]["certainty"]
                }
                
                # Add optional fields if present
                for field in ["source", "sourceType", "page", "paragraph"]:
                    if field in item and item[field] is not None:
                        doc[field] = item[field]
                
                # Parse metadata if present
                if "metadata" in item and item["metadata"]:
                    try:
                        doc["metadata"] = json.loads(item["metadata"])
                    except json.JSONDecodeError:
                        doc["metadata"] = item["metadata"]
                
                documents.append(doc)
        
        return documents
    
    except Exception as e:
        logger.error(f"Error searching vector database: {str(e)}")
        raise

async def delete_document(doc_id: str) -> bool:
    """
    Delete a document from the vector database.
    
    Args:
        doc_id: The document ID
        
    Returns:
        bool: True if deletion was successful
    """
    client = get_vector_client()
    
    try:
        client.data_object.delete(
            uuid=doc_id,
            class_name=DOCUMENT_CLASS_NAME
        )
        
        logger.info(f"Deleted document {doc_id} from vector database")
        return True
    
    except Exception as e:
        logger.error(f"Error deleting document from vector database: {str(e)}")
        raise

async def batch_add_documents(
    documents: List[Dict[str, Any]]
) -> List[str]:
    """
    Add multiple documents to the vector database in a batch.
    
    Args:
        documents: List of document dictionaries with keys:
                  text, source, source_type, page, paragraph, metadata
        
    Returns:
        List[str]: List of document IDs
    """
    client = get_vector_client()
    ensure_schema_exists()
    
    doc_ids = []
    
    try:
        with client.batch as batch:
            for doc in documents:
                # Generate a deterministic ID
                content_hash = hashlib.md5(doc["text"].encode()).hexdigest()
                source_str = str(doc.get("source", ""))
                doc_id = generate_uuid5(source_str + content_hash)
                
                # Prepare the document properties
                properties = {
                    "content": doc["text"],
                }
                
                if "source" in doc:
                    properties["source"] = doc["source"]
                
                if "source_type" in doc:
                    properties["sourceType"] = doc["source_type"]
                
                if "page" in doc:
                    properties["page"] = doc["page"]
                
                if "paragraph" in doc:
                    properties["paragraph"] = doc["paragraph"]
                
                if "metadata" in doc:
                    properties["metadata"] = json.dumps(doc["metadata"])
                
                # Add to batch
                batch.add_data_object(
                    data_object=properties,
                    class_name=DOCUMENT_CLASS_NAME,
                    uuid=doc_id
                )
                
                doc_ids.append(doc_id)
        
        logger.info(f"Added {len(doc_ids)} documents to vector database")
        return doc_ids
    
    except Exception as e:
        logger.error(f"Error batch adding documents to vector database: {str(e)}")
        raise
