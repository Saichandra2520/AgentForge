"""Local runner for the multi-agent supervisor template."""

from __future__ import annotations

from agents.supervisor import run_supervisor_workflow


def main() -> None:
    print("Multi-Agent Supervisor CLI is ready. Type 'exit' to quit.")
    while True:
        task = input("\\nTask: ").strip()
        if task.lower() in {"exit", "quit"}:
            print("Goodbye")
            break
        if not task:
            continue
        answer = run_supervisor_workflow(task)
        print(f"\\nFinal Answer:\n{answer}")


if __name__ == "__main__":
    main()