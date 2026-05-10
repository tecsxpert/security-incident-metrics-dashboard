from __future__ import annotations

from pathlib import Path


PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class PromptNotFoundError(FileNotFoundError):
    pass


def load_prompt_template(name: str) -> str:
    prompt_path = PROMPTS_DIR / name
    if not prompt_path.is_file():
        raise PromptNotFoundError(f"Prompt template not found: {name}")

    return prompt_path.read_text(encoding="utf-8")
