#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "generate.py"
SCANNER_PATH = (
    ROOT
    / "security"
    / "secret-scanner"
    / ".codex"
    / "hooks"
    / "secret-scanner.py"
)


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GENERATOR = load_module("aitmpl_codex_generator", GENERATOR_PATH)
SCANNER = load_module("aitmpl_codex_secret_scanner", SCANNER_PATH)


def secret_pattern(description: str) -> re.Pattern[str]:
    pattern = next(
        pattern
        for pattern, pattern_description, _severity in SCANNER.SECRET_PATTERNS
        if pattern_description == description
    )
    return re.compile(pattern)


def scanner_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment.pop("CODEX_CWD", None)
    environment.pop("CODEX_PROJECT_DIR", None)
    environment["PYTHONIOENCODING"] = "utf-8"
    return environment


def run_scanner(payload: dict, environment: dict[str, str] | None = None):
    return subprocess.run(
        [sys.executable, str(SCANNER_PATH)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment or scanner_environment(),
        timeout=15,
        check=False,
    )


class SecretPatternTests(unittest.TestCase):
    def test_cloudflare_token_assignments_match_with_or_without_quotes(self):
        pattern = secret_pattern("Cloudflare API Token")
        token = "A" * 40

        assignments = (
            f"CLOUDFLARE_API_TOKEN={token}",
            f"export CLOUDFLARE_API_TOKEN={token}",
            f"CF_API_TOKEN={token}",
            f"CLOUDFLARE_API_TOKEN='{token}'",
            f'CLOUDFLARE_API_TOKEN="{token}"',
            f'"CLOUDFLARE_API_TOKEN": "{token}"',
        )

        for assignment in assignments:
            with self.subTest(assignment=assignment[:40]):
                self.assertIsNotNone(pattern.search(assignment))

    def test_cloudflare_pattern_ignores_integrity_hashes_and_resource_ids(self):
        pattern = secret_pattern("Cloudflare API Token")
        hash_value = "cf" + ("1" * 62)

        safe_values = (
            hash_value,
            f'"integrity": "sha256-{hash_value}"',
            f'"resource_id": "{hash_value}"',
            f'CLOUDFLARE_BUILD_HASH="{hash_value}"',
        )

        for safe_value in safe_values:
            with self.subTest(safe_value=safe_value[:40]):
                self.assertIsNone(pattern.search(safe_value))

    def test_uuid_pattern_requires_credential_assignment_context(self):
        pattern = secret_pattern("Potential UUID Credential")
        uuid_value = "-".join(("12345678", "1234", "1234", "1234", "123456789abc"))

        self.assertIsNone(pattern.search(uuid_value))
        self.assertIsNotNone(pattern.search(f"API_KEY={uuid_value}"))
        self.assertIsNotNone(pattern.search(f'CLIENT_SECRET="{uuid_value}"'))

    def test_openssh_pattern_is_runtime_equivalent_without_self_detection(self):
        marker = "-----BEGIN OPENSSH " + "PRIVATE KEY-----"
        pattern = secret_pattern("OpenSSH Private Key")

        self.assertIsNotNone(pattern.search(marker))
        findings = SCANNER.scan_file(str(SCANNER_PATH))
        self.assertFalse(
            any(finding["description"] == "OpenSSH Private Key" for finding in findings)
        )

    def test_deno_lock_is_excluded(self):
        with tempfile.TemporaryDirectory(prefix="secret-scanner-deno-lock-") as tmpdir:
            lockfile = Path(tmpdir) / "deno.lock"
            lockfile.write_text(
                "API_KEY=" + ("A" * 40),
                encoding="utf-8",
            )

            self.assertEqual(SCANNER.scan_file(str(lockfile)), [])


class GeneratorDurabilityTests(unittest.TestCase):
    def setUp(self):
        self.generated = SCANNER_PATH.read_text(encoding="utf-8")
        self.upstream_like = self.generated
        for label, original, replacement in GENERATOR.SECRET_SCANNER_REPLACEMENTS:
            with self.subTest(label=label):
                self.assertEqual(self.generated.count(replacement), 1)
            self.upstream_like = self.upstream_like.replace(replacement, original, 1)

    def test_generator_recreates_the_committed_scanner(self):
        self.assertEqual(
            GENERATOR.adapt_secret_scanner(self.upstream_like),
            self.generated,
        )

    def test_generator_fails_closed_when_an_anchor_is_missing(self):
        _label, original, _replacement = GENERATOR.SECRET_SCANNER_REPLACEMENTS[0]
        missing_anchor = self.upstream_like.replace(original, "", 1)

        with self.assertRaisesRegex(SystemExit, "expected one Cloudflare token pattern"):
            GENERATOR.adapt_secret_scanner(missing_anchor)

    def test_generator_fails_closed_when_an_anchor_is_duplicated(self):
        _label, original, _replacement = GENERATOR.SECRET_SCANNER_REPLACEMENTS[0]

        with self.assertRaisesRegex(SystemExit, "expected one Cloudflare token pattern"):
            GENERATOR.adapt_secret_scanner(self.upstream_like + original)


class RepositoryContextTests(unittest.TestCase):
    def commit_payload(self, cwd: str | None = None) -> dict:
        payload = {"tool_input": {"command": "git commit -m scanner-test"}}
        if cwd is not None:
            payload["cwd"] = cwd
        return payload

    def test_non_commit_command_does_not_require_repository_context(self):
        result = run_scanner({"tool_input": {"command": "git status"}})

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_commit_without_repository_context_is_blocked(self):
        result = run_scanner(self.commit_payload())

        self.assertEqual(result.returncode, 2)
        self.assertIn("Could not resolve the triggering Git repository", result.stderr)

    def test_commit_with_missing_repository_context_is_blocked(self):
        missing = str(Path(tempfile.gettempdir()) / "missing-secret-scanner-repository")
        result = run_scanner(self.commit_payload(missing))

        self.assertEqual(result.returncode, 2)
        self.assertIn("Could not resolve the triggering Git repository", result.stderr)

    def test_commit_with_non_git_context_is_blocked(self):
        with tempfile.TemporaryDirectory(prefix="secret-scanner-non-git-") as tmpdir:
            result = run_scanner(self.commit_payload(tmpdir))

        self.assertEqual(result.returncode, 2)
        self.assertIn("Could not resolve the triggering Git repository", result.stderr)

    def test_scanner_uses_repository_root_from_nested_context(self):
        with tempfile.TemporaryDirectory(prefix="secret-scanner-repository-") as tmpdir:
            repository = Path(tmpdir) / "repository"
            nested = repository / "nested"
            nested.mkdir(parents=True)
            subprocess.run(
                ["git", "init", str(repository)],
                capture_output=True,
                check=True,
            )

            safe_file = repository / "safe.txt"
            safe_file.write_text("safe value\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(repository), "add", "safe.txt"],
                capture_output=True,
                check=True,
            )

            result = run_scanner(self.commit_payload(str(nested)))

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_scanner_blocks_an_unquoted_cloudflare_token(self):
        with tempfile.TemporaryDirectory(prefix="secret-scanner-known-bad-") as tmpdir:
            repository = Path(tmpdir) / "repository"
            repository.mkdir()
            subprocess.run(
                ["git", "init", str(repository)],
                capture_output=True,
                check=True,
            )

            bad_file = repository / "credentials.txt"
            bad_file.write_text(
                "export CLOUDFLARE_API_TOKEN=" + ("A" * 40),
                encoding="utf-8",
            )
            subprocess.run(
                ["git", "-C", str(repository), "add", "credentials.txt"],
                capture_output=True,
                check=True,
            )

            result = run_scanner(self.commit_payload(str(repository)))

        self.assertEqual(result.returncode, 2)
        self.assertIn("Potential secrets detected", result.stderr)


if __name__ == "__main__":
    unittest.main()
