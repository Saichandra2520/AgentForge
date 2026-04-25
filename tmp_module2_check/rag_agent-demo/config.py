"""Project configuration for rag_agent-demo."""

from pathlib import Path

PROJECT_NAME = "rag_agent-demo"
TEMPLATE = "rag_agent"
LLM_PROVIDER = "groq"
MODEL_NAME = "llama-3.3-70b-versatile"
BASE_DIR = Path(__file__).resolve().parent