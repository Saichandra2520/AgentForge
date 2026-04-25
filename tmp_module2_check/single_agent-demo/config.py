"""Project configuration for single_agent-demo."""

from pathlib import Path

PROJECT_NAME = "single_agent-demo"
TEMPLATE = "single_agent"
LLM_PROVIDER = "groq"
MODEL_NAME = "llama-3.3-70b-versatile"
BASE_DIR = Path(__file__).resolve().parent