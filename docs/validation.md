# Validation

Run the package checks with Python 3.10 or later:

```sh
python3 -m unittest discover -s tests -v
```

The tests cover complete copies, repeat installs, conflicting existing skills, instruction backups, trigger preservation, project paths, and configuration directories. They also build both release archives, verify their manifests, and install from an extracted package in a clean project.

Tests create isolated temporary folders. They do not use inbox tools or modify the actual user's agent instructions. Temporary folders remain available for inspection.

Build release files:

```sh
python3 scripts/build_release.py --output dist
```

The builder uses a fixed file list. It produces a full package ZIP, a skill-only ZIP, and `SHA256SUMS`. Each archive also has a file hash manifest. It refuses existing output files. Use a new output directory for a second build.

The skill-only ZIP has one top-level `business-email-formatting/` folder. It contains the license, skill, metadata, and both reference files. Upload support depends on the host. The full ZIP also contains the installer, documentation, and tests.

The source checks do not measure model quality, email response rates, or actual Gmail and Outlook rendering. Use the [behavioral review cases](review-cases.md) with your agent. Preview an authorized draft in the intended client when email rendering matters.

The GitHub Actions workflow defines checks for Linux, macOS, and Windows. A local test run does not establish that those remote jobs have passed.

## Local release check on 2026-10-28

- All 17 package tests pass on macOS with Python 3.14.
- The skill-creator validator accepts the skill.
- Skills CLI 1.7.4 discovers the skill from the local repository.
- A clean project install through that CLI succeeds for Codex, Claude Code, and Cursor targets.
- The copied files match the source bytes. Cursor and Codex use the shared `.agents/skills` copy in that test.
- The release archives install without access to the original checkout.

The GitHub network install and remote CI remain untested until publication. No model session in another host or live email client is tested by these package checks.
