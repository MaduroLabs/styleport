import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
EXTRACTOR = SKILLS_ROOT / "frontend-style-extractor"
ADAPTER = SKILLS_ROOT / "frontend-style-adapter"
EXAMPLE_BUNDLE = EXTRACTOR / "assets" / "example-bundle"
REQUIRED_BUNDLE_FILES = (
    "manifest.json",
    "tokens.json",
    "rules.json",
    "README.md",
    "typography.md",
    "layout-rules.md",
    "component-rules.md",
    "interaction-rules.md",
    "responsive-rules.md",
)


def parse_frontmatter(path):
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise AssertionError(f"missing frontmatter: {path}")
    _, header, _ = content.split("---", 2)
    values = {}
    for line in header.strip().splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip("\"'")
    return values


def run_validator(script, bundle):
    return subprocess.run(
        [sys.executable, str(script), str(bundle)],
        capture_output=True,
        text=True,
        check=False,
    )


class PackagingTests(unittest.TestCase):
    def test_skill_structure_and_metadata(self):
        for skill in (EXTRACTOR, ADAPTER):
            self.assertTrue((skill / "SKILL.md").is_file())
            metadata = parse_frontmatter(skill / "SKILL.md")
            self.assertEqual(metadata["name"], skill.name)
            self.assertTrue(metadata["description"])
            self.assertLessEqual(len(metadata["name"]), 64)
            self.assertLessEqual(len(metadata["description"]), 1024)
            self.assertRegex(metadata["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

    def test_contract_and_validator_copies_are_identical(self):
        for relative in (
            "references/CONTRACT.md",
            "scripts/style_inventory.py",
            "scripts/validate_bundle.py",
        ):
            extractor_bytes = (EXTRACTOR / relative).read_bytes()
            adapter_bytes = (ADAPTER / relative).read_bytes()
            self.assertEqual(
                hashlib.sha256(extractor_bytes).digest(),
                hashlib.sha256(adapter_bytes).digest(),
                relative,
            )

    def test_example_bundle_has_required_tree(self):
        for relative in REQUIRED_BUNDLE_FILES:
            path = EXAMPLE_BUNDLE / relative
            self.assertTrue(path.is_file(), path)
            self.assertFalse(path.is_symlink(), path)

    def test_example_bundle_validates_with_both_skills(self):
        for skill in (EXTRACTOR, ADAPTER):
            result = run_validator(skill / "scripts" / "validate_bundle.py", EXAMPLE_BUNDLE)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("VALID bundle v1.0.0", result.stdout)

    def test_invalid_token_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            bundle = Path(temporary_dir) / "bundle"
            bundle.mkdir()
            for relative in REQUIRED_BUNDLE_FILES:
                source = EXAMPLE_BUNDLE / relative
                destination = bundle / relative
                destination.write_bytes(source.read_bytes())
            rules_path = bundle / "rules.json"
            rules = json.loads(rules_path.read_text(encoding="utf-8"))
            rules["rules"][0]["tokenRefs"].append("color.missing")
            rules_path.write_text(json.dumps(rules), encoding="utf-8")
            result = run_validator(EXTRACTOR / "scripts" / "validate_bundle.py", bundle)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown token", result.stderr)

    def test_inventory_reports_synthetic_source(self):
        source = REPO_ROOT / "tests" / "fixtures" / "source-mini"
        result = subprocess.run(
            [sys.executable, str(EXTRACTOR / "scripts" / "style_inventory.py"), str(source)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        inventory = json.loads(result.stdout)
        self.assertIn("--brand-primary", inventory["customProperties"])
        self.assertIn("background-color", inventory["declarations"])
        self.assertIn("640px", " ".join(inventory["mediaQueries"]))
        self.assertIn("react", inventory["stack"]["frameworkHints"])


if __name__ == "__main__":
    unittest.main()
