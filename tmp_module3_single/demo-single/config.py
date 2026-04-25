"""LLM configuration for the generated single-agent project."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").strip().lower()
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile").strip()


def get_chat_model():
    """Return a configured chat model for the selected provider."""
    if LLM_PROVIDER == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY. Set it in your .env file.")
        return ChatGroq(model=MODEL_NAME, api_key=api_key)

    if LLM_PROVIDER == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY. Set it in your .env file.")
        return ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=api_key)

    if LLM_PROVIDER == "azure":
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT") or MODEL_NAME
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
        if not api_key or not endpoint:
            raise ValueError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT in .env.")
        return AzureChatOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            azure_deployment=deployment,
            api_version=api_version,
        )

    if LLM_PROVIDER == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return ChatOllama(model=MODEL_NAME, base_url=base_url)

    raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")