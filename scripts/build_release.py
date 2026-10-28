#!/usr/bin/env python3
"""Build allowlisted source and skill ZIPs with SHA-256 manifests."""
from pathlib import Path
import argparse
import hashlib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "business-email-formatting"
VERSION = "1.0.0"
SKILL_FILES = (
    "SKILL.md", "LICENSE", "agents/openai.yaml",
    "references/examples.md", "references/delivery.md",
)
PACKAGE_FILES = (
    "README.md", "LICENSE", "NOTICE.md", ".gitignore", "install.py",
    "docs/installation.md", "docs/linkedin-post.md", "docs/validation.md",
    "docs/review-cases.md", ".github/workflows/check.yml",
    "scripts/build_release.py", "tests/test_install.py", "tests/test_release.py",
) + tuple(f"skills/{NAME}/{p}" for p in SKILL_FILES)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def archive(path: Path, base: Path, names: tuple, prefix: str):
    entries = {}
    for name in names:
        source = base / name
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"Missing file or unexpected link: {source}")
        entries[name] = source.read_bytes()
    manifest = "".join(f"{digest(data)}  {name}\n" for name, data in sorted(entries.items()))
    with zipfile.ZipFile(path, "x", zipfile.ZIP_DEFLATED) as output:
        for name, data in sorted(entries.items()):
            output.writestr(prefix + "/" + name, data)
        output.writestr(prefix + "/MANIFEST.sha256", manifest)


def build(output: Path) -> list[Path]:
    paths = [output / f"{NAME}-{VERSION}.zip", output / f"{NAME}-skill-{VERSION}.zip", output / "SHA256SUMS"]
    if any(p.exists() for p in paths):
        raise ValueError("Release files already exist. Select a new output directory.")
    # Validate the complete source set before producing an archive.
    for name in PACKAGE_FILES:
        p = ROOT / name
        if not p.is_file() or p.is_symlink():
            raise ValueError(f"Missing file or unexpected link: {p}")
    output.mkdir(parents=True, exist_ok=True)
    archive(paths[0], ROOT, PACKAGE_FILES, f"{NAME}-{VERSION}")
    archive(paths[1], ROOT / "skills" / NAME, SKILL_FILES, NAME)
    with paths[2].open("x", encoding="utf-8") as stream:
        for p in paths[:2]:
            stream.write(f"{digest(p.read_bytes())}  {p.name}\n")
    return paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    for path in build(args.output):
        print(path)
