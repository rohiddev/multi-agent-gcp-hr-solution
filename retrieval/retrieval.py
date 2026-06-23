"""
Retrieval layer — enterprise HR knowledge.

Supports multiple backends selectable by RETRIEVAL_BACKEND in .env:
  agent_search      -> Google Agent Builder / Vertex AI Search (managed)
  rag_engine        -> Vertex AI RAG Engine (managed RAG pipeline)
  vertex_ai_search  -> Vertex AI Search (enterprise search)
  vector_search     -> Vertex AI Vector Search (custom embeddings)
  stub              -> deterministic local stub (development / MVP)

In production, pick the backend that matches your document sources and
compliance requirements. The agents call `retrieve()` without knowing which
backend is underneath.
"""

import logging
from typing import Optional
from config import (
    RETRIEVAL_BACKEND,
    AGENT_SEARCH_APP,
    RAG_ENGINE_CORPUS,
    VERTEX_AI_INDEX,
    VECTOR_INDEX_ENDPOINT,
    EMBEDDING_MODEL,
)

logger = logging.getLogger(__name__)


def retrieve(query: str, top_k: int = 5, allowed_sources: Optional[list[str]] = None) -> list[dict]:
    """Retrieve relevant HR documents from the configured enterprise backend.

    Args:
        query: Natural language question.
        top_k: Number of results to return.
        allowed_sources: Optional filter, e.g. ["hr_policy", "benefits", "payroll"].

    Returns:
        list of dicts with content, source, and score.
    """
    allowed_sources = allowed_sources or []
    logger.info("retrieve backend=%s query=%s top_k=%d", RETRIEVAL_BACKEND, query, top_k)

    if RETRIEVAL_BACKEND == "stub":
        return _retrieve_stub(query, top_k, allowed_sources)
    if RETRIEVAL_BACKEND == "agent_search":
        return _retrieve_agent_search(query, top_k)
    if RETRIEVAL_BACKEND == "rag_engine":
        return _retrieve_rag_engine(query, top_k)
    if RETRIEVAL_BACKEND == "vertex_ai_search":
        return _retrieve_vertex_ai_search(query, top_k)
    if RETRIEVAL_BACKEND == "vector_search":
        return _retrieve_vector_search(query, top_k)

    # Should never reach here because config validates the backend at startup.
    raise ValueError(f"Unsupported retrieval backend: {RETRIEVAL_BACKEND}")


def _retrieve_stub(query: str, top_k: int, allowed_sources: list[str]) -> list[dict]:
    """Development stub that returns sample documents matching keywords."""
    logger.warning("Using stub retrieval backend. Set RETRIEVAL_BACKEND in .env for production.")

    sample_docs = [
        {
            "content": "Full-time employees accrue 20 PTO days per year. Unused days carry over up to 40 days.",
            "source": "hr_policy/pto_policy.md",
            "score": 0.95,
        },
        {
            "content": "Parental leave provides up to 12 weeks of paid leave for eligible parents.",
            "source": "hr_policy/parental_leave.md",
            "score": 0.92,
        },
        {
            "content": "The company offers medical, dental, vision, and a 401(k) match of up to 4%.",
            "source": "benefits/overview.md",
            "score": 0.90,
        },
        {
            "content": "Payroll is processed bi-weekly. Direct deposit is required for all employees.",
            "source": "payroll/faq.md",
            "score": 0.88,
        },
        {
            "content": "Procurement requests over $5,000 require manager and finance approval.",
            "source": "procurement/procedures.md",
            "score": 0.85,
        },
        {
            "content": "All contracts and NDAs must be reviewed by the legal team before signing.",
            "source": "legal/intake.md",
            "score": 0.84,
        },
        {
            "content": "Annual compliance training is mandatory for all employees and must be completed by December 31.",
            "source": "compliance/training.md",
            "score": 0.83,
        },
        {
            "content": "Report building access issues to facilities via the internal portal or email facilities@company.com.",
            "source": "facilities/access.md",
            "score": 0.82,
        },
    ]

    lowered = query.lower()
    matches = [doc for doc in sample_docs if any(term in lowered for term in doc["source"].lower().split("/"))]

    # If no source-specific match, fall back to keyword matching in content.
    if not matches:
        keywords = lowered.split()
        matches = [doc for doc in sample_docs if any(kw in doc["content"].lower() for kw in keywords)]

    # Apply source filter if provided.
    if allowed_sources:
        matches = [doc for doc in matches if any(src in doc["source"] for src in allowed_sources)]

    # Sort by score descending and return top_k.
    matches = sorted(matches, key=lambda d: d["score"], reverse=True)[:top_k]
    return matches if matches else []


def _retrieve_agent_search(query: str, top_k: int) -> list[dict]:
    """Google Agent Builder / Vertex AI Search retrieval."""
    if not AGENT_SEARCH_APP:
        raise EnvironmentError("AGENT_SEARCH_APP is required for agent_search backend.")
    logger.info("Agent Search retrieve app=%s", AGENT_SEARCH_APP)
    # TODO: implement google.cloud.discoveryengine client call.
    return [{"content": "[Agent Search] Placeholder result", "source": AGENT_SEARCH_APP, "score": 0.0}]


def _retrieve_rag_engine(query: str, top_k: int) -> list[dict]:
    """Vertex AI RAG Engine retrieval."""
    if not RAG_ENGINE_CORPUS:
        raise EnvironmentError("RAG_ENGINE_CORPUS is required for rag_engine backend.")
    logger.info("RAG Engine retrieve corpus=%s", RAG_ENGINE_CORPUS)
    # TODO: implement aiplatform.rag retrieval call.
    return [{"content": "[RAG Engine] Placeholder result", "source": RAG_ENGINE_CORPUS, "score": 0.0}]


def _retrieve_vertex_ai_search(query: str, top_k: int) -> list[dict]:
    """Vertex AI Search retrieval."""
    if not VERTEX_AI_INDEX:
        raise EnvironmentError("VERTEX_AI_INDEX is required for vertex_ai_search backend.")
    logger.info("Vertex AI Search retrieve index=%s", VERTEX_AI_INDEX)
    # TODO: implement Vertex AI Search lookup.
    return [{"content": "[Vertex AI Search] Placeholder result", "source": VERTEX_AI_INDEX, "score": 0.0}]


def _retrieve_vector_search(query: str, top_k: int) -> list[dict]:
    """Vertex AI Vector Search retrieval."""
    if not VECTOR_INDEX_ENDPOINT:
        raise EnvironmentError("VECTOR_INDEX_ENDPOINT is required for vector_search backend.")
    logger.info("Vector Search retrieve endpoint=%s model=%s", VECTOR_INDEX_ENDPOINT, EMBEDDING_MODEL)
    # TODO: embed query and query matching engine index.
    return [{"content": "[Vector Search] Placeholder result", "source": VECTOR_INDEX_ENDPOINT, "score": 0.0}]
