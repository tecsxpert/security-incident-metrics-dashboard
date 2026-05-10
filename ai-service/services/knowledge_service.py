from __future__ import annotations

import logging
import os
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class KnowledgeDocument:
    doc_id: str
    title: str
    content: str


DOMAIN_KNOWLEDGE: list[KnowledgeDocument] = [
    KnowledgeDocument(
        "auth-001",
        "Repeated VPN failures followed by success",
        "Repeated failed VPN authentication followed by a successful login from an unfamiliar source can indicate credential compromise.",
    ),
    KnowledgeDocument(
        "auth-002",
        "Unknown IP remote access",
        "Remote access from an unknown IP should be correlated with user location, device posture, VPN logs, and active sessions.",
    ),
    KnowledgeDocument(
        "auth-003",
        "Suspicious geography",
        "Login attempts from unusual countries, impossible travel patterns, or unfamiliar networks increase authentication incident severity.",
    ),
    KnowledgeDocument(
        "malware-001",
        "EDR malware alert",
        "Endpoint malware detections require triage of process trees, file hashes, network connections, and containment status.",
    ),
    KnowledgeDocument(
        "malware-002",
        "Malware spread risk",
        "Multiple endpoint detections in a short period may indicate propagation, shared payload delivery, or lateral movement.",
    ),
    KnowledgeDocument(
        "phish-001",
        "Credential phishing",
        "Credential harvesting emails can lead to account takeover and should be correlated with suspicious login events.",
    ),
    KnowledgeDocument(
        "priv-001",
        "Privilege escalation signal",
        "Unexpected privilege changes after suspicious authentication indicate a higher likelihood of active compromise.",
    ),
    KnowledgeDocument(
        "contain-001",
        "Account containment",
        "For suspected account compromise, revoke active sessions, reset credentials, and review MFA state before re-enabling access.",
    ),
    KnowledgeDocument(
        "contain-002",
        "Network containment",
        "Suspicious IPs can be blocked or rate-limited after preserving logs and confirming the source is not trusted infrastructure.",
    ),
    KnowledgeDocument(
        "report-001",
        "SOC report synthesis",
        "Incident reports should identify recurring patterns, common indicators, severity concentration, and operational next steps without inventing facts.",
    ),
]


def initialize_ai_knowledge() -> bool:
    if os.getenv("AI_KNOWLEDGE_ENABLED", "true").lower() != "true":
        logger.info("ai_knowledge_preload_skipped reason=disabled")
        return False

    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
    except Exception:
        logger.warning(
            "ai_knowledge_preload_skipped reason=optional_dependencies_missing "
            "packages=sentence-transformers,chromadb"
        )
        return False

    model_name = os.getenv("AI_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    chroma_dir = os.getenv("CHROMA_DB_DIR", ".chroma")
    collection_name = os.getenv("CHROMA_COLLECTION", "security_incident_knowledge")

    try:
        model = SentenceTransformer(model_name)
        client = chromadb.PersistentClient(path=chroma_dir)
        collection = client.get_or_create_collection(collection_name)

        ids = [doc.doc_id for doc in DOMAIN_KNOWLEDGE]
        documents = [doc.content for doc in DOMAIN_KNOWLEDGE]
        embeddings = model.encode(documents, normalize_embeddings=True).tolist()
        metadatas = [{"title": doc.title} for doc in DOMAIN_KNOWLEDGE]

        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        logger.info(
            "ai_knowledge_preloaded collection=%s documents=%s model=%s",
            collection_name,
            len(DOMAIN_KNOWLEDGE),
            model_name,
        )
        return True
    except Exception:
        logger.exception("ai_knowledge_preload_failed")
        return False
