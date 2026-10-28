# Business Email Formatting

Give your AI agent a reusable format for business email: short paragraphs, useful lists, clear requests, and spacing that survives the email tool.

The skill handles requests, updates, meeting recaps, proposal follow-ups, and short replies. It preserves the facts and adapts the structure to the message. A two-sentence reply stays short.

## Before and after

**Before**

> Hi Alex, please send the approved account list and the report date range. I can finish the estimate after I receive both. Data purchases are separate from the project fee. Thanks, Sam

**After**

> Hi Alex,
>
> Please send:
>
> - The approved account list.
> - The report date range.
>
> I can finish the estimate after I receive both. Data purchases are separate from the project fee.
>
> Thanks,  
> Sam

This is a fictional example. The format makes the two inputs visible and keeps the fee exclusion.

## Install

With Node.js and the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add priorodds-mesh8/business-email-formatting --skill business-email-formatting -g
```

Choose your agent in the installer. `-g` installs for your user across projects. The CLI currently requires Node.js 22.20 or later. It is a third-party installer; review its prompts and current requirements.

For an offline install, download this repository as a ZIP and extract it. From the extracted folder, run:

```sh
python3 install.py --agent claude --with-trigger
```

Use `codex` instead of `claude` for Codex. Use `cursor` without `--with-trigger` for a global Cursor install. On Windows, use `py -3` instead of `python3`.

The bundled installer needs Python 3.10 or later and no extra packages. It copies the complete skill. `--with-trigger` also adds a small email rule and backs up existing instructions. It refuses a different existing skill. It does not send email or change account settings.

See [installation](docs/installation.md) for project installs, Cursor User Rules, manual copying, updates, and removal.

## Use it

In Codex:

```text
Use $business-email-formatting to format this email. Preserve the facts and commitments:

[paste the email]
```

In Claude Code:

```text
/business-email-formatting Format this email for a client. Preserve the facts and commitments:

[paste the email]
```

In other agents, select `business-email-formatting` from the skill picker or request it by name. If it is not visible, start a new session.

The skill description supports automatic selection. Use the optional trigger for an explicit instruction to apply it to business email.

## What it changes

- Short paragraphs, with one topic per paragraph.
- Bullets for related items and numbers for ordered steps or separate questions.
- Takeaways and section labels when a longer message needs them.
- Clear actions, with owners and dates when the source supplies them.
- HTML paragraphs and lists, or plain text separators, matched to the email tool.

It preserves names, amounts, dates, links, commitments, exclusions, and uncertainty. For a format-only request, it preserves wording. It does not force headings, bullets, or a summary into every message.

The skill works alone. It also works alongside your existing voice rules, [STE100](https://github.com/priorodds-mesh8/ste100-writing-skill), or anti-slop instructions. Those are optional and are not bundled.

## Compatibility and limits

The package follows the Agent Skills folder format. Local installation paths are documented for Codex, Claude Code, and Cursor. An optional Grok path follows a local convention and has no verified public compatibility claim.

Installation checks do not prove automatic activation in every agent. Local installation also does not install a skill into a hosted chat account. Consult your host's skill upload or sync instructions.

This is an instruction skill, not an email client. It has no inbox access, API key, tracking code, or send function. Your agent and its email tools control those capabilities. It does not guarantee reply rates or identical rendering in every client.

See [validation](docs/validation.md) for the checks and their limits, and [sources](NOTICE.md) for the research behind the rules.

## License

MIT. Copyright 2026 Joel Lang. See [LICENSE](LICENSE).
