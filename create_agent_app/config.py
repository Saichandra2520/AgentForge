
from dataclasses import dataclass, field
from enum import Enum
from typing import List


class LLMProvider(str, Enum):
    GROQ = "groq"
    GEMINI = "gemini"
    AZURE = "azure"
    OLLAMA = "ollama"


class TemplateType(str, Enum):
    REACT_AGENT = "react_agent"
    RAG_AGENT = "rag_agent"
    MULTI_AGENT = "multi_agent"
    CONVERSATIONAL = "conversational"
    HITL = "hitl"


class VectorStore(str, Enum):
    CHROMA = "chroma"
    QDRANT = "qdrant"


@dataclass
class ProjectConfig:
    # Core
    project_name: str = ""
    template: TemplateType = TemplateType.REACT_AGENT
    llm_provider: LLMProvider = LLMProvider.GROQ

    # Features — affect which files are generated
    include_api: bool = True
    include_streaming: bool = True
    include_docker: bool = False
    include_tests: bool = True
    include_observability: bool = False

    # RAG-specific
    vector_store: VectorStore = VectorStore.CHROMA
    include_semantic_cache: bool = False
    include_guards: bool = True
    include_hybrid_retrieval: bool = True

    # Agent description — used in README and system prompt
    agent_description: str = "A helpful AI assistant"

    # Tools to pre-install
    tools: List[str] = field(default_factory=lambda: ["web_search"])

    @property
    def project_slug(self) -> str:
        return self.project_name.lower().replace(" ", "_").replace("-", "_")

    def to_jinja_context(self) -> dict:
        return {
            "project_name": self.project_name,
            "project_slug": self.project_slug,
            "template": self.template.value,
            "llm_provider": self.llm_provider.value,
            "include_api": self.include_api,
            "include_streaming": self.include_streaming,
            "include_docker": self.include_docker,
            "include_tests": self.include_tests,
            "include_observability": self.include_observability,
            "vector_store": self.vector_store.value,
            "include_semantic_cache": self.include_semantic_cache,
            "include_guards": self.include_guards,
            "include_hybrid_retrieval": self.include_hybrid_retrieval,
            "agent_description": self.agent_description,
            "tools": self.tools,
        }
