
"""Interactive prompt flow for create-agent-app."""

from questionary import Choice
import questionary
from rich.console import Console
from rich.table import Table

from .config import ProjectConfig, LLMProvider, TemplateType, VectorStore


def run_prompts() -> ProjectConfig:
    """Run the interactive setup flow and return a ProjectConfig."""
    console = Console()

    # REQUIRED QUESTIONS

    # 1. project_name
    project_name = questionary.text(
        "What is your project name?",
        validate=lambda x: len(x.strip()) > 0
    ).ask()

    # 2. template
    template = questionary.select(
        "Which agent template?",
        choices=[
            Choice("ReAct Agent — reasoning + tool use loop", "react_agent"),
            Choice("RAG Agent — document Q&A with retrieval", "rag_agent"),
            Choice("Multi-Agent Supervisor — orchestrator + workers", "multi_agent"),
            Choice("Conversational Agent — persistent memory", "conversational"),
            Choice("Human-in-the-Loop — agent pauses for approval", "hitl"),
        ]
    ).ask()

    # 3. llm_provider
    llm_provider = questionary.select(
        "Which LLM provider?",
        choices=[
            Choice("Groq (free tier — recommended)", "groq"),
            Choice("Google Gemini (free tier)", "gemini"),
            Choice("Azure OpenAI", "azure"),
            Choice("Ollama (local, fully free)", "ollama"),
        ]
    ).ask()

    # 4. include_api
    include_api = questionary.confirm(
        "Include FastAPI backend?",
        default=True
    ).ask()

    # 5. include_streaming (ONLY ASK if include_api is True)
    include_streaming = True
    if include_api:
        include_streaming = questionary.confirm(
            "Include streaming support?",
            default=True
        ).ask()

    # 6. tools
    tools = questionary.checkbox(
        "Which tools to pre-install?",
        choices=[
            Choice("web_search", value="web_search"),
            Choice("calculator", value="calculator"),
            Choice("file_reader", value="file_reader"),
        ]
    ).ask()
    # Ensure at least one tool is selected
    if not tools:
        tools = ["web_search"]

    # RAG-SPECIFIC (ONLY ASK if template == "rag_agent")
    include_semantic_cache = False
    include_guards = True
    if template == "rag_agent":
        # 7. include_semantic_cache
        include_semantic_cache = questionary.confirm(
            "Include semantic cache? (requires Upstash Redis free tier)",
            default=False
        ).ask()

        # 8. include_guards
        include_guards = questionary.confirm(
            "Include input/output security guards?",
            default=True
        ).ask()

    # OPTIONAL SECTION
    # 9. Configure optional features?
    configure_optional = questionary.confirm(
        "Configure optional features?",
        default=False
    ).ask()

    if configure_optional:
        # 9a. include_docker
        include_docker = questionary.confirm(
            "Add Docker support?",
            default=False
        ).ask()

        # 9b. include_tests
        include_tests = questionary.confirm(
            "Scaffold test files?",
            default=True
        ).ask()

        # 9c. include_observability
        include_observability = questionary.confirm(
            "Add Langfuse observability?",
            default=False
        ).ask()

        # 9d. agent_description
        agent_description = questionary.text(
            "Describe your agent in one line:",
            default="A helpful AI assistant"
        ).ask()
    else:
        include_docker = False
        include_tests = True
        include_observability = False
        agent_description = "A helpful AI assistant"

    # Build the ProjectConfig
    config = ProjectConfig(
        project_name=project_name,
        template=TemplateType(template),
        llm_provider=LLMProvider(llm_provider),
        include_api=include_api,
        include_streaming=include_streaming,
        include_docker=include_docker,
        include_tests=include_tests,
        include_observability=include_observability,
        include_semantic_cache=include_semantic_cache,
        include_guards=include_guards,
        agent_description=agent_description,
        tools=tools,
    )

    # Print summary table using rich
    _print_summary_table(console, config)

    return config


def _print_summary_table(console: Console, config: ProjectConfig) -> None:
    """Print a rich Table summarising all choices."""
    table = Table(title="Project Configuration Summary")

    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    table.add_row("Project Name", config.project_name)
    table.add_row("Template", config.template.value)
    table.add_row("LLM Provider", config.llm_provider.value)
    table.add_row("Include API", str(config.include_api))
    table.add_row("Include Streaming", str(config.include_streaming))
    table.add_row("Tools", ", ".join(config.tools))

    if config.template == TemplateType.RAG_AGENT:
        table.add_row("Include Semantic Cache", str(config.include_semantic_cache))
        table.add_row("Include Security Guards", str(config.include_guards))

    table.add_row("Include Docker", str(config.include_docker))
    table.add_row("Include Tests", str(config.include_tests))
    table.add_row("Include Observability", str(config.include_observability))
    table.add_row("Agent Description", config.agent_description)

    console.print(table)
