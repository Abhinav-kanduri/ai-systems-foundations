"""
Document Intake Agent - parses documents and extracts fields.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import json

from agents.base import BaseAgent
from schemas.agents import DocumentIntakeInput, DocumentIntakeOutput
from schemas.evidence import EvidenceItem, EvidenceType


class DocumentIntakeAgent(BaseAgent):
    """Agent for document intake, parsing, and field extraction."""
    
    def __init__(self):
        super().__init__(
            agent_name="DocumentIntakeAgent",
            agent_version="1.0.0"
        )
        self.min_confidence = 0.7
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute document intake and extraction.
        
        Args:
            application_id: Loan application ID
            applicant_id: Applicant ID
            document_ids: List of document IDs
            documents_content: Optional dict of document content
            
        Returns:
            dict: Extracted fields, missing documents, confidence scores
        """
        application_id = kwargs.get("application_id")
        documents = kwargs.get("documents_content", {})
        
        self.validate_input(kwargs, ["application_id", "applicant_id"])
        
        extracted_fields = {}
        document_quality = {}
        missing_documents = []
        processing_errors = []
        
        # Simulate document extraction
        if documents:
            for doc_id, content in documents.items():
                try:
                    # Simulate OCR/parsing
                    parsed = self._parse_document(doc_id, content)
                    extracted_fields.update(parsed["fields"])
                    document_quality[doc_id] = parsed["confidence"]
                except Exception as e:
                    processing_errors.append(f"Failed to parse {doc_id}: {str(e)}")
        
        # Check for required documents
        required_docs = {"paystub", "id_proof"}
        provided_docs = set(doc_id.lower() for doc_id in documents.keys())
        missing = required_docs - provided_docs
        if missing:
            missing_documents = list(missing)
        
        # Overall confidence
        quality_scores = list(document_quality.values())
        overall_confidence = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
        
        result = {
            "application_id": application_id,
            "extracted_fields": extracted_fields,
            "missing_documents": missing_documents,
            "document_quality": document_quality,
            "processing_errors": processing_errors,
            "confidence": overall_confidence,
            "requires_manual_review": len(missing_documents) > 0 or overall_confidence < self.min_confidence
        }
        
        return result
    
    def _parse_document(self, doc_id: str, content: str) -> Dict[str, Any]:
        """
        Simulate document parsing.
        
        Args:
            doc_id: Document ID
            content: Document content/text
            
        Returns:
            dict: Parsed fields and confidence
        """
        # Simulated extraction based on document type
        doc_type = doc_id.lower()
        
        if "paystub" in doc_type:
            return {
                "fields": {
                    "gross_monthly_salary": 5000.0,
                    "employer_name": "Tech Corp Inc",
                    "employment_start_date": "2020-01-15",
                    "ytd_earnings": 55000.0
                },
                "confidence": 0.95
            }
        elif "bank" in doc_type:
            return {
                "fields": {
                    "account_holder_name": "John Doe",
                    "average_monthly_deposit": 5100.0,
                    "account_age_months": 36,
                    "account_type": "checking"
                },
                "confidence": 0.92
            }
        elif "id" in doc_type.lower():
            return {
                "fields": {
                    "document_type": "driver_license",
                    "state": "CA",
                    "valid": True
                },
                "confidence": 0.97
            }
        else:
            return {
                "fields": {
                    "document_extracted": True
                },
                "confidence": 0.75
            }
    
    def generate_evidence(self, agent_output: Dict[str, Any]) -> EvidenceItem:
        """Generate evidence record from agent output."""
        return EvidenceItem(
            agent_name=self.agent_name,
            agent_version=self.agent_version,
            evidence_type=EvidenceType.DOCUMENT_EXTRACTION,
            description=f"Extracted {len(agent_output['extracted_fields'])} fields from documents",
            key_findings=agent_output["extracted_fields"],
            supporting_data={
                "document_quality": agent_output["document_quality"],
                "missing_documents": agent_output["missing_documents"],
                "errors": agent_output.get("processing_errors", [])
            },
            confidence=agent_output["confidence"],
            source_refs=["document_intake_service"],
            reasoning=f"Parsed documents with {agent_output['confidence']:.0%} confidence"
        )
