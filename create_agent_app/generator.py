
"""Jinja2-based project structure generator."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from create_agent_app.config import ProjectConfig
import subprocess
from rich.console import Console
from rich.table import Table


class ProjectGenerator:

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.template_dir = Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            keep_trailing_newline=True,
        )

    def generate(self, output_dir: Path) -> int:
        project_dir = output_dir / self.config.project_name
        project_dir.mkdir(parents=True, exist_ok=False)

        context = self.config.to_jinja_context()
        file_count = 0

        # 1. Render shared templates
        file_count += self._render_shared(project_dir, context)

        # 2. Render template-specific files
        template_map = {
            "react_agent": self._render_react_agent,
            "rag_agent": self._render_rag_agent,
            "multi_agent": self._render_multi_agent,
            "conversational": self._render_conversational,
            "hitl": self._render_hitl,
        }
        file_count += template_map[self.config.template.value](project_dir, context)

        # 3. Create __init__.py in all Python package dirs
        self._create_init_files(project_dir)

        # 4. Create data directory
        (project_dir / "data").mkdir(exist_ok=True)
        (project_dir / "data" / ".gitkeep").touch()

        # 5. Initialize git
        self._init_git(project_dir)

        # 6. Generation summary
        console = Console()
        summary = Table(title="Generation Summary")
        summary.add_column("Setting", style="cyan")
        summary.add_column("Value", style="green")
        summary.add_row("Project", self.config.project_name)
        summary.add_row("Template", self.config.template.value)
        summary.add_row("LLM Provider", self.config.llm_provider.value)
        summary.add_row("API Backend", "Yes" if self.config.include_api else "No")
        summary.add_row("Tests", "Yes" if self.config.include_tests else "No")
        summary.add_row("Docker", "Yes" if self.config.include_docker else "No")
        summary.add_row("Files Generated", str(file_count))
        console.print(summary)

        return file_count

    def _render_file(self, template_path: str, output_path: Path, context: dict) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        template = self.env.get_template(template_path)
        output_path.write_text(template.render(**context), encoding="utf-8")

    def _render_shared(self, project_dir: Path, context: dict) -> int:
        count = 0
        shared_dir = self.template_dir / "shared"
        for j2_file in shared_dir.glob("*.j2"):
            output_name = j2_file.stem
            self._render_file(f"shared/{j2_file.name}", project_dir / output_name, context)
            count += 1
        return count

    def _render_template_dir(
        self,
        source_dir: Path,
        project_dir: Path,
        context: dict,
        skip_dirs: list[str],
        skip_files: list[str],
    ) -> int:
        count = 0
        for j2_file in source_dir.rglob("*.j2"):
            rel_path = j2_file.relative_to(source_dir)
            rel_posix = rel_path.as_posix()

            if any(part in skip_dirs for part in rel_path.parts):
                continue

            if j2_file.name in skip_files or rel_posix in skip_files:
                continue

            output_rel = rel_path.with_suffix("")
            self._render_file(
                f"{source_dir.name}/{rel_posix}",
                project_dir / output_rel,
                context,
            )
            count += 1
        return count

    def _create_init_files(self, project_dir: Path) -> None:
        for dir_path in project_dir.rglob("*"):
            if dir_path.is_dir():
                init = dir_path / "__init__.py"
                if not init.exists():
                    init.write_text("", encoding="utf-8")

    def _init_git(self, project_dir: Path) -> None:
        try:
            subprocess.run(["git", "init"], cwd=project_dir,
                           capture_output=True, check=False)
        except Exception:
            pass

    def _render_react_agent(self, project_dir: Path, context: dict) -> int:
        skip_dirs = []
        skip_files = []

        if not context.get("include_api", True):
            skip_dirs.append("api")
        if not context.get("include_tests", True):
            skip_dirs.append("tests")
        if not context.get("include_docker", False):
            skip_files.extend(["Dockerfile.j2", "docker-compose.yml.j2"])

        return self._render_template_dir(
            source_dir=self.template_dir / "react_agent",
            project_dir=project_dir,
            context=context,
            skip_dirs=skip_dirs,
            skip_files=skip_files,
        )

    def _render_rag_agent(self, project_dir: Path, context: dict) -> int:
        skip_dirs = []
        skip_files = []

        if not context.get("include_api", True):
            skip_dirs.append("api")
        if not context.get("include_guards", True):
            skip_dirs.append("security")
        if not context.get("include_tests", True):
            skip_dirs.append("tests")
        if not context.get("include_docker", False):
            skip_files.extend(["Dockerfile.j2", "docker-compose.yml.j2"])
        if not context.get("include_semantic_cache", False):
            skip_files.append("memory/semantic_cache.py.j2")

        return self._render_template_dir(
            source_dir=self.template_dir / "rag_agent",
            project_dir=project_dir,
            context=context,
            skip_dirs=skip_dirs,
            skip_files=skip_files,
        )

    def _render_multi_agent(self, project_dir: Path, context: dict) -> int:
        skip_dirs = []
        skip_files = []

        if not context.get("include_api", True):
            skip_dirs.append("api")
        if not context.get("include_tests", True):
            skip_dirs.append("tests")
        if not context.get("include_docker", False):
            skip_files.extend(["Dockerfile.j2", "docker-compose.yml.j2"])

        return self._render_template_dir(
            source_dir=self.template_dir / "multi_agent",
            project_dir=project_dir,
            context=context,
            skip_dirs=skip_dirs,
            skip_files=skip_files,
        )

    def _render_conversational(self, project_dir: Path, context: dict) -> int:
        return self._render_react_agent(project_dir, context)

    def _render_hitl(self, project_dir: Path, context: dict) -> int:
        return self._render_multi_agent(project_dir, context)
