# Installation

Install the complete `skills/business-email-formatting/` folder. Its reference files are part of the skill.

## Install from GitHub

```sh
npx skills add priorodds-mesh8/business-email-formatting --skill business-email-formatting -g
```

Choose the agents to install. To select one directly, add `-a codex`, `-a claude-code`, or `-a cursor`. Omit `-g` for a project installation. The Skills CLI controls its own update behavior and prompts. It can collect usage telemetry; see its [documentation](https://github.com/vercel-labs/skills#telemetry).

This command works after the public repository is available. To test a downloaded copy before publication:

```sh
npx skills add . --skill business-email-formatting --list
```

## Use the bundled installer

Requires Python 3.10 or later. No pip install is needed. Run these commands from the extracted repository or clone.

```sh
python3 install.py --agent codex --with-trigger
python3 install.py --agent claude --with-trigger
python3 install.py --agent cursor
```

Use the command for your agent. On Windows, replace `python3` with `py -3`.

| Agent | Default user skill directory | Optional global trigger |
| --- | --- | --- |
| Codex | `~/.agents/skills/business-email-formatting/` | `$CODEX_HOME/AGENTS.md`, or `~/.codex/AGENTS.md` |
| Claude Code | `~/.claude/skills/business-email-formatting/` | `~/.claude/CLAUDE.md` |
| Cursor | `~/.cursor/skills/business-email-formatting/` | Paste the printed snippet into Cursor User Rules |
| Grok, experimental path | `~/.grok/skills/business-email-formatting/` | `~/.grok/AGENTS.md`; verify in your host |

If `CLAUDE_CONFIG_DIR` is set, the installer uses it for Claude's skill and global instruction file. The Codex skill location remains `~/.agents/skills/`; `CODEX_HOME` selects its global instruction directory.

Without `--with-trigger`, the installer changes only the skill folder and prints an optional trigger. With that flag, it adds one marked section and saves a byte-for-byte backup of any prior instruction file. Repeating an identical install makes no changes.

Global Cursor User Rules are managed in the application. The installer does not claim that a home-directory `.mdc` file is a global User Rule. Open Cursor's rule settings and paste the printed snippet there if you want an explicit trigger.

For one existing project:

```sh
python3 install.py --agent codex --project "/path/to/project" --with-trigger
```

Project skills use `.agents/skills/`, `.claude/skills/`, `.cursor/skills/`, or `.grok/skills/` under that project. Project triggers use `AGENTS.md`, `CLAUDE.md`, or a dedicated Cursor rule. A project trigger applies only within that project.

## Manual install

Copy the full skill folder into your host's documented skill directory. No script is needed. Do not copy only `SKILL.md`.

Optional instruction text:

```text
When composing, rewriting, reviewing, or preparing business email for delivery,
use the business-email-formatting skill. Preserve existing voice and language rules.
Apply it to drafts in chat and email tools. Do not use it for mailbox searches
or summaries of received email.
```

If your host cannot discover skills, add the actual installed `SKILL.md` path to that instruction. Local files must be accessible to the host.

## Confirm installation

Start a new session if needed. Ask the agent to use the skill on a fictional email. Confirm that it uses useful paragraph breaks and preserves prices, dates, exclusions, and uncertainty.

A suggested test:

```text
Format this email without changing its facts. Do not send it:
Hi Alex, please send the approved account list and the report date range.
I can finish the estimate after I receive both. Data purchases are separate
from the project fee. Thanks, Sam
```

See [review cases](review-cases.md) for more examples. Confirm real email rendering separately when you use an authorized draft or send workflow.

## Update or remove

The bundled installer does not overwrite a different installation. Move the old skill folder outside all active skill directories, then run the installer again. Keep the backup until the new version works. Do not keep two versions with the same skill name in active directories.

For removal, move the skill outside the active directories. Remove only the section between `business-email-formatting:start` and `business-email-formatting:end` from the instruction file. Preserve later edits to that file. For Cursor User Rules, remove the snippet through the application.

If you used the Skills CLI, use its documented update and removal commands instead. Do not combine installation methods for the same agent without reviewing existing paths.

## Host documentation

- [Codex skill locations](https://learn.chatgpt.com/docs/build-skills).
- [Claude Code skills](https://code.claude.com/docs/en/skills).
- [Cursor skills](https://cursor.com/docs/skills).
- [Skills CLI commands](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).

These locations were checked on 2026-10-28. Hosted sessions, remote workers, and account-level skill uploads can use different locations.
