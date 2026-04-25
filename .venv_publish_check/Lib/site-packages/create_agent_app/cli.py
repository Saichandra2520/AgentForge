"""CLI entrypoint for create-agent-app."""

import typer
from rich.console import Console
from rich.panel import Panel

from .generator import GenerationAbortedError, create_project_structure
from .prompts import run_prompts

console = Console()


def _next_steps(template: str) -> str:
    common = (
        "1. `cd {project}`\n"
        "2. `python -m venv .venv`\n"
        "3. Activate venv and run `pip install -r requirements.txt`\n"
        "4. Copy `.env.example` to `.env` and fill provider keys\n"
    )
    if template == "multi_agent":
        run_hint = "5. Run `python main.py` to execute the supervisor + workers workflow."
    elif template == "rag_agent":
        run_hint = "5. Run `python main.py` to ingest docs and start the RAG chat loop."
    else:
        run_hint = "5. Run `python main.py` to start the single-agent CLI."
    return common + run_hint


def create(project_name: str | None = typer.Argument(None)) -> None:
    """Run the interactive create flow."""
    try:
        config = run_prompts(project_name)
        with console.status("[bold cyan]Generating project files...", spinner="dots"):
            create_project_structure(config)

        console.print("[bold green]Project scaffold created successfully.[/bold green]")
        console.print(
            Panel.fit(
                _next_steps(config.template).format(project=config.project_name),
                title="Next Steps",
                border_style="green",
            )
        )
        typer.echo(config.to_dict())
    except GenerationAbortedError as exc:
        console.print(f"[yellow]{exc}[/yellow]")
        raise typer.Exit(code=1) from exc
    except (FileExistsError, ValueError) as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc
    except KeyboardInterrupt as exc:
        console.print("[yellow]Prompt cancelled. No files were generated.[/yellow]")
        raise typer.Exit(code=1) from exc


def main() -> None:
    typer.run(create)


if __name__ == "__main__":
    main()
