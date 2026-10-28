import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.home = Path(tempfile.mkdtemp(prefix="email-skill-test-")).resolve()

    def install(self, agent="codex", **kwargs):
        return installer.install(agent, home=self.home, env={}, **kwargs)

    def test_all_agent_copies_are_complete(self):
        for agent in installer.AGENTS:
            result = self.install(agent)
            self.assertEqual(installer.files(result["skill"]), installer.files(installer.SOURCE))
            self.assertIsNone(result["instruction"])

    def test_instructions_are_opt_in(self):
        self.install()
        self.assertFalse((self.home / ".codex/AGENTS.md").exists())

    def test_existing_instruction_bytes_are_preserved_and_backed_up(self):
        path = self.home / ".codex/AGENTS.md"
        path.parent.mkdir()
        old = b"# Existing rules\r\nPreserve caf\xc3\xa9 names.\r\n"
        path.write_bytes(old)
        result = self.install(with_trigger=True)
        self.assertTrue(path.read_bytes().startswith(old))
        self.assertEqual(result["backup"].read_bytes(), old)
        self.assertIn(str(result["skill"] / "SKILL.md"), path.read_text())

    def test_repeat_install_does_not_duplicate_trigger_or_backup(self):
        first = self.install(with_trigger=True)
        before = first["instruction"].read_bytes()
        second = self.install(with_trigger=True)
        self.assertEqual(before, second["instruction"].read_bytes())
        self.assertTrue(second["already_installed"])
        self.assertIsNone(second["backup"])

    def test_modified_skill_is_not_overwritten(self):
        first = self.install()
        custom = first["skill"] / "references/examples.md"
        custom.write_text("My local examples.")
        with self.assertRaisesRegex(ValueError, "different skill"):
            self.install(with_trigger=True)
        self.assertEqual(custom.read_text(), "My local examples.")
        self.assertFalse((self.home / ".codex/AGENTS.md").exists())

    def test_changed_trigger_stops_before_skill_copy(self):
        rule = self.home / ".claude/CLAUDE.md"
        rule.parent.mkdir()
        old = installer.START + "\nMy customized rule.\n" + installer.END
        rule.write_text(old)
        with self.assertRaisesRegex(ValueError, "existing trigger differs"):
            self.install("claude", with_trigger=True)
        self.assertEqual(rule.read_text(), old)
        self.assertFalse((self.home / ".claude/skills").exists())

    def test_manual_trigger_is_not_duplicated(self):
        rule = self.home / ".codex/AGENTS.md"
        rule.parent.mkdir()
        rule.write_text("Use business-email-formatting for client email.")
        with self.assertRaisesRegex(ValueError, "already mentions"):
            self.install(with_trigger=True)
        self.assertFalse((self.home / ".agents/skills").exists())

    def test_project_install_with_spaces(self):
        project = self.home / "Team Project"
        project.mkdir()
        result = self.install("claude", project=project, with_trigger=True)
        self.assertEqual(result["skill"], project / ".claude/skills" / installer.NAME)
        self.assertEqual(result["instruction"], project / "CLAUDE.md")
        self.assertFalse((self.home / ".claude").exists())

    def test_missing_project_stops_without_creating_it(self):
        project = self.home / "missing"
        with self.assertRaisesRegex(ValueError, "must already exist"):
            self.install(project=project)
        self.assertFalse(project.exists())

    def test_cursor_global_trigger_requires_user_rules(self):
        with self.assertRaisesRegex(ValueError, "User Rules"):
            self.install("cursor", with_trigger=True)
        self.assertFalse((self.home / ".cursor").exists())

    def test_cursor_project_rule(self):
        result = self.install("cursor", project=self.home, with_trigger=True)
        self.assertIn("alwaysApply: true", result["instruction"].read_text())
        self.assertEqual(result["instruction"].suffix, ".mdc")

    def test_configuration_directories(self):
        codex = self.home / "custom codex"
        claude = self.home / "custom claude"
        result = installer.install("codex", home=self.home, env={"CODEX_HOME": str(codex)}, with_trigger=True)
        self.assertEqual(result["instruction"], codex / "AGENTS.md")
        self.assertEqual(result["skill"], self.home / ".agents/skills" / installer.NAME)
        result = installer.install("claude", home=self.home, env={"CLAUDE_CONFIG_DIR": str(claude)}, with_trigger=True)
        self.assertEqual(result["instruction"], claude / "CLAUDE.md")
        self.assertEqual(result["skill"], claude / "skills" / installer.NAME)

    def test_skill_symlink_is_not_followed_or_replaced(self):
        external = self.home / "external"
        external.mkdir()
        (external / "SKILL.md").write_text("Private skill.")
        dest = self.home / ".agents/skills" / installer.NAME
        dest.parent.mkdir(parents=True)
        try:
            dest.symlink_to(external, target_is_directory=True)
        except OSError:
            self.skipTest("This system cannot create symlinks.")
        with self.assertRaises(ValueError):
            self.install()
        self.assertTrue(dest.is_symlink())
        self.assertEqual((external / "SKILL.md").read_text(), "Private skill.")


if __name__ == "__main__":
    unittest.main()
