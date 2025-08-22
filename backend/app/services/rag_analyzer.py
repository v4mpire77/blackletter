"""
RAG Analyzer Service

Integrates RAG capabilities with contract analysis for enhanced legal document processing.
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import uuid

from ..core.llm_adapter import LLMAdapter
from .rag_store import rag_store, TextChunk
from .vague_detector import VagueTermsDetector
from .gemini_judge import gemini_judge

class RAGAnalyzer:
    """Enhanced contract analyzer using RAG capabilities."""
    
    def __init__(self):
        self.llm_adapter = LLMAdapter()
        self.vague_detector = VagueTermsDetector()
    
    async def analyze_contract_with_rag(self, doc_id: str, text: str, 
                                      metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform comprehensive contract analysis using RAG.
        
        Args:
            doc_id: Document identifier
            text: Contract text
            metadata: Document metadata
            
        Returns:
            Analysis results with RAG-enhanced insights
        """
        try:
            # Store document in RAG store
            chunks = await rag_store.store_document(doc_id, text, metadata)
            
            # Perform basic contract analysis
            basic_analysis = await self.llm_adapter.analyze_contract(text)
            
            # Find vague terms
            vague_hits = self.vague_detector.find_vague_spans(text)
            
            # Enhanced analysis using RAG
            rag_insights = await self._generate_rag_insights(doc_id, text, vague_hits)
            
            # Generate compliance analysis
            compliance_analysis = await self._analyze_compliance(doc_id, text)
            
            # Generate risk assessment
            risk_assessment = await self._assess_risks(doc_id, text)
            
            return {
                "doc_id": doc_id,
                "basic_analysis": basic_analysis,
                "rag_insights": rag_insights,
                "compliance_analysis": compliance_analysis,
                "risk_assessment": risk_assessment,
                "vague_terms_found": len(vague_hits),
                "chunks_created": len(chunks),
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "doc_id": doc_id,
                "error": str(e),
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
    
    async def _generate_rag_insights(self, doc_id: str, text: str, 
                                   vague_hits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights using RAG capabilities."""
        insights = {
            "key_clauses": [],
            "important_dates": [],
            "parties_involved": [],
            "financial_terms": [],
            "termination_conditions": []
        }
        
        # Query for key contract elements
        queries = [
            "What are the key clauses and obligations in this contract?",
            "What are the important dates and deadlines mentioned?",
            "Who are the parties involved in this contract?",
            "What are the financial terms and payment conditions?",
            "What are the termination conditions and exit clauses?"
        ]
        
        for query in queries:
            try:
                # Get query embedding
                query_embedding = await self.llm_adapter.get_embeddings([query])
                if not query_embedding:
                    continue
                
                # Retrieve relevant chunks
                similar_chunks = await rag_store.retrieve_similar(
                    query_embedding[0], top_k=3, doc_id=doc_id
                )
                
                if similar_chunks:
                    # Generate insight using context
                    context_chunks = [chunk.text for chunk, score in similar_chunks]
                    insight = await self.llm_adapter.generate_with_context(query, context_chunks)
                    
                    # Categorize insight
                    if "date" in query.lower() or "deadline" in query.lower():
                        insights["important_dates"].append(insight)
                    elif "party" in query.lower() or "involved" in query.lower():
                        insights["parties_involved"].append(insight)
                    elif "financial" in query.lower() or "payment" in query.lower():
                        insights["financial_terms"].append(insight)
                    elif "termination" in query.lower() or "exit" in query.lower():
                        insights["termination_conditions"].append(insight)
                    else:
                        insights["key_clauses"].append(insight)
                        
            except Exception as e:
                print(f"Error generating insight for query '{query}': {e}")
        
        return insights
    
    async def _analyze_compliance(self, doc_id: str, text: str) -> Dict[str, Any]:
        """Analyze contract for compliance issues."""
        compliance_queries = [
            "What GDPR compliance issues might exist in this contract?",
            "Are there any data protection or privacy concerns?",
            "What regulatory compliance requirements are mentioned?",
            "Are there any potential legal or regulatory risks?"
        ]
        
        compliance_issues = []
        
        for query in compliance_queries:
            try:
                query_embedding = await self.llm_adapter.get_embeddings([query])
                if not query_embedding:
                    continue
                
                similar_chunks = await rag_store.retrieve_similar(
                    query_embedding[0], top_k=5, doc_id=doc_id
                )
                
                if similar_chunks:
                    context_chunks = [chunk.text for chunk, score in similar_chunks]
                    analysis = await self.llm_adapter.generate_with_context(query, context_chunks)
                    
                    compliance_issues.append({
                        "query": query,
                        "analysis": analysis,
                        "relevant_chunks": len(similar_chunks)
                    })
                    
            except Exception as e:
                print(f"Error analyzing compliance for query '{query}': {e}")
        
        return {
            "compliance_issues": compliance_issues,
            "total_issues_identified": len(compliance_issues)
        }
    
    async def _assess_risks(self, doc_id: str, text: str) -> Dict[str, Any]:
        """Assess contract risks using RAG."""
        risk_queries = [
            "What are the main risks and liabilities in this contract?",
            "What are the potential financial risks?",
            "What are the operational risks mentioned?",
            "What are the legal risks and potential disputes?"
        ]
        
        risk_assessment = {
            "financial_risks": [],
            "operational_risks": [],
            "legal_risks": [],
            "overall_risk_level": "Medium"
        }
        
        total_risk_score = 0
        
        for query in risk_queries:
            try:
                query_embedding = await self.llm_adapter.get_embeddings([query])
                if not query_embedding:
                    continue
                
                similar_chunks = await rag_store.retrieve_similar(
                    query_embedding[0], top_k=5, doc_id=doc_id
                )
                
                if similar_chunks:
                    context_chunks = [chunk.text for chunk, score in similar_chunks]
                    risk_analysis = await self.llm_adapter.generate_with_context(query, context_chunks)
                    
                    # Categorize risk
                    if "financial" in query.lower():
                        risk_assessment["financial_risks"].append(risk_analysis)
                        total_risk_score += 1
                    elif "operational" in query.lower():
                        risk_assessment["operational_risks"].append(risk_analysis)
                        total_risk_score += 1
                    elif "legal" in query.lower():
                        risk_assessment["legal_risks"].append(risk_analysis)
                        total_risk_score += 2  # Legal risks weighted higher
                        
            except Exception as e:
                print(f"Error assessing risks for query '{query}': {e}")
        
        # Determine overall risk level
        if total_risk_score >= 6:
            risk_assessment["overall_risk_level"] = "High"
        elif total_risk_score >= 3:
            risk_assessment["overall_risk_level"] = "Medium"
        else:
            risk_assessment["overall_risk_level"] = "Low"
        
        risk_assessment["total_risk_score"] = total_risk_score
        
        return risk_assessment
    
    async def query_contract(self, doc_id: str, query: str, 
                           include_context: bool = True) -> Dict[str, Any]:
        """
        Query a specific contract using RAG.
        
        Args:
            doc_id: Document identifier
            query: Natural language query
            include_context: Whether to include context chunks in response
            
        Returns:
            Query response with relevant information
        """
        try:
            # Get query embedding
            query_embedding = await self.llm_adapter.get_embeddings([query])
            if not query_embedding:
                return {"error": "Failed to generate query embedding"}
            
            # Retrieve similar chunks
            similar_chunks = await rag_store.retrieve_similar(
                query_embedding[0], top_k=5, doc_id=doc_id
            )
            
            if not similar_chunks:
                return {
                    "answer": "No relevant information found in the contract for this query.",
                    "chunks": [],
                    "query": query
                }
            
            # Generate response using context
            context_chunks = [chunk.text for chunk, score in similar_chunks]
            answer = await self.llm_adapter.generate_with_context(query, context_chunks)
            
            response = {
                "answer": answer,
                "query": query,
                "total_chunks_retrieved": len(similar_chunks)
            }
            
            if include_context:
                chunk_details = []
                for chunk, score in similar_chunks:
                    chunk_details.append({
                        "id": chunk.id,
                        "text": chunk.text[:300] + "..." if len(chunk.text) > 300 else chunk.text,
                        "page": chunk.page,
                        "similarity_score": round(score, 3),
                        "start_pos": chunk.start_pos,
                        "end_pos": chunk.end_pos
                    })
                response["chunks"] = chunk_details
            
            return response
            
        except Exception as e:
            return {"error": f"Error processing query: {str(e)}"}
    
    async def compare_contracts(self, doc_ids: List[str], 
                              comparison_criteria: List[str]) -> Dict[str, Any]:
        """
        Compare multiple contracts using RAG.
        
        Args:
            doc_ids: List of document identifiers
            comparison_criteria: List of criteria to compare
            
        Returns:
            Comparison results
        """
        comparison_results = {}
        
        for criterion in comparison_criteria:
            criterion_results = {}
            
            for doc_id in doc_ids:
                try:
                    # Query each contract for the criterion
                    query = f"What are the {criterion} in this contract?"
                    result = await self.query_contract(doc_id, query, include_context=False)
                    
                    criterion_results[doc_id] = {
                        "answer": result.get("answer", "No information found"),
                        "chunks_retrieved": result.get("total_chunks_retrieved", 0)
                    }
                    
                except Exception as e:
                    criterion_results[doc_id] = {
                        "error": str(e),
                        "chunks_retrieved": 0
                    }
            
            comparison_results[criterion] = criterion_results
        
        return {
            "comparison_criteria": comparison_criteria,
            "documents_compared": doc_ids,
            "results": comparison_results
        }
    
    async def generate_summary_report(self, doc_id: str) -> Dict[str, Any]:
        """Generate a comprehensive summary report for a contract."""
        try:
            # Get document chunks
            chunks = rag_store.get_document_chunks(doc_id)
            if not chunks:
                return {"error": "Document not found or no chunks available"}
            
            # Generate comprehensive summary
            summary_queries = [
                "Provide a comprehensive executive summary of this contract",
                "What are the key terms and conditions?",
                "What are the main obligations of each party?",
                "What are the critical dates and deadlines?",
                "What are the key risks and considerations?"
            ]
            
            summary_sections = {}
            
            for query in summary_queries:
                try:
                    result = await self.query_contract(doc_id, query, include_context=False)
                    section_name = query.split(" of ")[-1].replace("?", "").lower()
                    summary_sections[section_name] = result.get("answer", "No information available")
                except Exception as e:
                    section_name = query.split(" of ")[-1].replace("?", "").lower()
                    summary_sections[section_name] = f"Error generating section: {str(e)}"
            
            return {
                "doc_id": doc_id,
                "total_chunks": len(chunks),
                "summary_sections": summary_sections,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Error generating summary report: {str(e)}"}

# Global instance
rag_analyzer = RAGAnalyzer()
