
"""Configuration models for project scaffolding prompts."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectConfig:
    """User-selected settings that define the scaffolded project."""

    project_name: str
    template: str
    llm_provider: str
    model_name: str
    output_dir: Path

    def to_dict(self) -> dict[str, str]:
        """Return a clean dictionary representation for CLI output."""
        return {
            "project_name": self.project_name,
            "template": self.template,
            "llm_provider": self.llm_provider,
            "model_name": self.model_name,
            "output_dir": str(self.output_dir),
        }
