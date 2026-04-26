import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from create_agent_app.prompts import run_prompts
from create_agent_app.generator import ProjectGenerator

app = typer.Typer(
    help="create-agent-app — Vite-style scaffolder for Agentic AI projects in Python"
)
console = Console()


@app.command()
def create(
    project_name: str = typer.Argument(
        None, help="Project name (optional, will prompt if not provided)"
    ),
    output_dir: Path = typer.Option(
        Path("."), "--output", "-o", help="Output directory"
    ),
):
    console.print(
        Panel.fit(
            "[bold blue]create-agent-app[/bold blue]\n"
            "[dim]Vite-style scaffolder for production Agentic AI projects[/dim]",
            border_style="blue",
        )
    )

    config = run_prompts()

    if project_name:
        config.project_name = project_name

    generator = ProjectGenerator(config)

    with console.status(f"[bold green]Generating {config.project_name}..."):
        try:
            file_count = generator.generate(output_dir)
        except FileExistsError:
            console.print(
                f"[bold red]Error:[/bold red] "
                f"Directory '{config.project_name}' already exists in {output_dir}"
            )
            raise typer.Exit(1)

    # Success summary
    table = Table(title="Project Created", show_header=False, box=None)
    table.add_column("Key", style="dim")
    table.add_column("Value", style="bold green")
    table.add_row("Project", config.project_name)
    table.add_row("Template", config.template.value)
    table.add_row("LLM Provider", config.llm_provider.value)
    table.add_row("Files generated", str(file_count or "—"))
    console.print(table)

    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"  [cyan]cd {config.project_name}[/cyan]")
    console.print("  [cyan]pip install -r requirements.txt[/cyan]")
    console.print("  [cyan]cp .env.example .env[/cyan]")
    console.print("  [cyan]# Add your API key to .env[/cyan]")
    console.print("  [cyan]python main.py[/cyan]")


if __name__ == "__main__":
    app()
