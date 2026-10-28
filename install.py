#!/usr/bin/env python3
"""Install the complete skill using only the Python standard library."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys
import uuid

ROOT = Path(__file__).resolve().parent
NAME = "business-email-formatting"
SOURCE = ROOT / "skills" / NAME
START = "<!-- business-email-formatting:start -->"
END = "<!-- business-email-formatting:end -->"
AGENTS = {"codex": ".agents", "claude": ".claude", "cursor": ".cursor", "grok": ".grok"}


def trigger_text(skill: Path) -> str:
    return (
        f"{START}\n"
        "## Business email formatting\n\n"
        "When composing, rewriting, reviewing, or preparing business email for delivery,\n"
        f"read `{(skill / 'SKILL.md').as_posix()}` and apply it.\n"
        "Preserve existing voice and language rules. Use short paragraphs, useful lists,\n"
        "and clear requests. Check the body format before an email tool call.\n"
        "Do not apply this trigger to mailbox searches or summaries of received email.\n"
        f"{END}\n"
    )


def files(folder: Path) -> dict[str, bytes]:
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError(f"Review the existing destination before installation: {folder}")
    result = {}
    for path in sorted(folder.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"A skill file is a link. Review it before installation: {path}")
        if path.is_file():
            result[path.relative_to(folder).as_posix()] = path.read_bytes()
    return result


def install(agent: str, project: Path | None = None, with_trigger: bool = False,
            home: Path | None = None, env: dict | None = None) -> dict:
    if agent not in AGENTS:
        raise ValueError("Choose codex, claude, cursor, or grok.")
    home = (home or Path.home()).resolve()
    env = os.environ if env is None else env
    if project is not None:
        base = project.expanduser().resolve()
        if not base.is_dir():
            raise ValueError("The project directory must already exist.")
        skill = base / AGENTS[agent] / "skills" / NAME
        instruction = base / ("CLAUDE.md" if agent == "claude" else "AGENTS.md")
        if agent == "cursor":
            instruction = base / ".cursor" / "rules" / f"{NAME}.mdc"
    else:
        config = home / AGENTS[agent]
        if agent == "claude" and env.get("CLAUDE_CONFIG_DIR"):
            config = Path(env["CLAUDE_CONFIG_DIR"]).expanduser().resolve()
        skill = config / "skills" / NAME
        instruction = config / "AGENTS.md"
        if agent == "codex":
            codex = Path(env.get("CODEX_HOME", str(home / ".codex"))).expanduser().resolve()
            instruction = codex / "AGENTS.md"
        elif agent == "claude":
            instruction = config / "CLAUDE.md"
        if agent == "cursor" and with_trigger:
            raise ValueError("For a global Cursor trigger, paste the printed snippet into User Rules. Run without --with-trigger.")

    source_files = files(SOURCE)
    exists = skill.exists() or skill.is_symlink()
    if exists and files(skill) != source_files:
        raise ValueError(f"A different skill already exists at {skill}. Move it to a backup folder, then retry.")

    block = trigger_text(skill)
    previous = b""
    updated = None
    if with_trigger:
        if instruction.is_symlink():
            raise ValueError(f"The instruction file is a link. Review it first: {instruction}")
        if instruction.exists():
            previous = instruction.read_bytes()
        text = previous.decode("utf-8")
        if START in text or END in text:
            if text.count(START) != 1 or text.count(END) != 1 or block not in text:
                raise ValueError(f"An existing trigger differs. Review it first: {instruction}")
        elif NAME in text:
            raise ValueError(f"This file already mentions the skill. Review its trigger first: {instruction}")
        else:
            if agent == "cursor":
                if previous:
                    raise ValueError(f"The Cursor rule already exists. Review it first: {instruction}")
                prefix = "---\ndescription: Format business email drafts and replies\nalwaysApply: true\n---\n\n"
                updated = (prefix + block).encode("utf-8")
            else:
                updated = previous + (b"\n\n" if previous else b"") + block.encode("utf-8")

    if not exists:
        skill.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(SOURCE, skill)

    backup = None
    if updated is not None:
        instruction.parent.mkdir(parents=True, exist_ok=True)
        if previous:
            backup = instruction.with_name(instruction.name + f".backup-{uuid.uuid4().hex[:10]}")
            with backup.open("xb") as stream:
                stream.write(previous)
        # Do not replace content that changed after preflight.
        current = instruction.read_bytes() if instruction.exists() else b""
        if current != previous:
            raise ValueError(f"The instruction file changed. The skill is installed; review the trigger manually: {instruction}")
        instruction.write_bytes(updated)

    return {"skill": skill, "instruction": instruction if with_trigger else None,
            "backup": backup, "trigger": block, "already_installed": exists}


def main() -> int:
    parser = argparse.ArgumentParser(description="Install business-email-formatting without replacing existing skills.")
    parser.add_argument("--agent", required=True, choices=AGENTS)
    parser.add_argument("--project", type=Path, help="Install into this existing project. Default: the current user's skill directory.")
    parser.add_argument("--with-trigger", action="store_true", help="Append an email trigger and preserve the prior instruction file in a backup.")
    args = parser.parse_args()
    try:
        result = install(args.agent, args.project, args.with_trigger)
    except (ValueError, OSError, UnicodeError) as exc:
        print(f"Installation stopped: {exc}", file=sys.stderr)
        return 2
    print(f"Skill ready: {result['skill']}")
    if result["instruction"]:
        print(f"Trigger ready: {result['instruction']}")
    else:
        print("Optional trigger for your agent's instructions:\n" + result["trigger"])
    if result["backup"]:
        print(f"Original instructions: {result['backup']}")
    print("Start a new agent session if the skill is not yet visible.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
