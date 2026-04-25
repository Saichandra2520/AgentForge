
"""Interactive prompt flow for create-agent-app."""

from pathlib import Path
import re

import questionary

from .config import ProjectConfig

PROJECT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9-]+$")
MAX_PROJECT_NAME_LENGTH = 50

TEMPLATE_CHOICES: list[questionary.Choice] = [
    questionary.Choice("Single Agent", value="single_agent"),
    questionary.Choice("Multi-Agent Supervisor", value="multi_agent"),
    questionary.Choice("RAG Agent", value="rag_agent"),
]

PROVIDER_CHOICES: list[questionary.Choice] = [
    questionary.Choice("Groq", value="groq"),
    questionary.Choice("Gemini", value="gemini"),
    questionary.Choice("Azure OpenAI", value="azure"),
    questionary.Choice("Ollama", value="ollama"),
]

MODEL_CHOICES: dict[str, list[questionary.Choice]] = {
    "groq": [
        questionary.Choice("llama-3.3-70b-versatile", value="llama-3.3-70b-versatile"),
        questionary.Choice("llama-3.1-8b-instant", value="llama-3.1-8b-instant"),
        questionary.Choice("mixtral-8x7b-32768", value="mixtral-8x7b-32768"),
    ],
    "gemini": [
        questionary.Choice("gemini-2.5-pro", value="gemini-2.5-pro"),
        questionary.Choice("gemini-2.5-flash", value="gemini-2.5-flash"),
        questionary.Choice("gemini-1.5-pro", value="gemini-1.5-pro"),
    ],
    "azure": [
        questionary.Choice("gpt-4o", value="gpt-4o"),
        questionary.Choice("gpt-4.1", value="gpt-4.1"),
        questionary.Choice("gpt-4o-mini", value="gpt-4o-mini"),
    ],
    "ollama": [
        questionary.Choice("llama3.1", value="llama3.1"),
        questionary.Choice("qwen2.5", value="qwen2.5"),
        questionary.Choice("mistral", value="mistral"),
    ],
}


def _validate_project_name(value: str) -> bool | str:
    if not value:
        return "Project name is required."
    if len(value) > MAX_PROJECT_NAME_LENGTH:
        return f"Project name must be {MAX_PROJECT_NAME_LENGTH} characters or fewer."
    if not PROJECT_NAME_PATTERN.fullmatch(value):
        return "Use only letters, numbers, and hyphens (no spaces or special characters)."
    return True


def _ask_required_text(message: str, default: str | None = None) -> str:
    result = questionary.text(message, default=default, validate=_validate_project_name).ask()
    if result is None:
        raise KeyboardInterrupt("Prompt cancelled by user.")
    return result


def _ask_choice(message: str, choices: list[questionary.Choice]) -> str:
    result = questionary.select(message, choices=choices).ask()
    if result is None:
        raise KeyboardInterrupt("Prompt cancelled by user.")
    return result


def _validate_provider_model(llm_provider: str, model_name: str) -> None:
    valid_models = {choice.value for choice in MODEL_CHOICES.get(llm_provider, [])}
    if model_name not in valid_models:
        valid_display = ", ".join(sorted(valid_models)) or "none"
        raise ValueError(
            f"Model '{model_name}' is not valid for provider '{llm_provider}'. "
            f"Supported models: {valid_display}"
        )


def run_prompts(project_name: str | None = None, output_dir: Path | None = None) -> ProjectConfig:
    """Collect all required scaffold configuration from CLI + interactive prompts."""
    if project_name and _validate_project_name(project_name) is True:
        final_project_name = project_name
    else:
        final_project_name = _ask_required_text("Project name:", default=project_name)

    template = _ask_choice("Choose a template:", TEMPLATE_CHOICES)
    llm_provider = _ask_choice("Choose an LLM provider:", PROVIDER_CHOICES)
    model_name = _ask_choice("Choose a model:", MODEL_CHOICES[llm_provider])
    _validate_provider_model(llm_provider, model_name)

    base_dir = output_dir or Path.cwd()
    return ProjectConfig(
        project_name=final_project_name,
        template=template,
        llm_provider=llm_provider,
        model_name=model_name,
        output_dir=base_dir / final_project_name,
    )
