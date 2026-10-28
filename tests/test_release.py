import hashlib
import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("builder", ROOT / "scripts/build_release.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix="email-skill-release-test-"))

    def test_archives_have_only_allowlisted_files_and_valid_hashes(self):
        paths = builder.build(self.work / "output")
        for path, expected in zip(paths[:2], (builder.PACKAGE_FILES, builder.SKILL_FILES)):
            with zipfile.ZipFile(path) as z:
                prefix = z.namelist()[0].split("/")[0]
                self.assertEqual(set(z.namelist()), {prefix + "/" + n for n in expected} | {prefix + "/MANIFEST.sha256"})
                for line in z.read(prefix + "/MANIFEST.sha256").decode().splitlines():
                    sha, name = line.split("  ", 1)
                    self.assertEqual(hashlib.sha256(z.read(prefix + "/" + name)).hexdigest(), sha)
        for line in paths[2].read_text().splitlines():
            sha, name = line.split("  ", 1)
            self.assertEqual(hashlib.sha256((paths[2].parent / name).read_bytes()).hexdigest(), sha)

    def test_extracted_package_installs_without_source_checkout(self):
        paths = builder.build(self.work / "output")
        with zipfile.ZipFile(paths[0]) as z:
            z.extractall(self.work / "extracted")
        package = next((self.work / "extracted").iterdir())
        project = self.work / "clean project"
        project.mkdir()
        result = subprocess.run([sys.executable, str(package / "install.py"), "--agent", "claude", "--project", str(project), "--with-trigger"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        installed = project / ".claude/skills" / builder.NAME
        for name in builder.SKILL_FILES:
            self.assertEqual((installed / name).read_bytes(), (package / "skills" / builder.NAME / name).read_bytes())
        self.assertIn(str(installed / "SKILL.md").replace("\\", "/"), (project / "CLAUDE.md").read_text())

    def test_build_does_not_replace_existing_archives(self):
        paths = builder.build(self.work)
        original = paths[0].read_bytes()
        with self.assertRaises(ValueError):
            builder.build(self.work)
        self.assertEqual(paths[0].read_bytes(), original)

    def test_skill_has_no_private_paths_and_all_references_exist(self):
        skill = ROOT / "skills" / builder.NAME
        for name in builder.SKILL_FILES:
            text = (skill / name).read_text()
            self.assertNotRegex(text, r"/Users/|ObsidianVault|[A-Z]:\\\\Users\\\\")
        for target in re.findall(r"\]\((references/[^)]+)\)", (skill / "SKILL.md").read_text()):
            self.assertTrue((skill / target).is_file())


if __name__ == "__main__":
    unittest.main()
