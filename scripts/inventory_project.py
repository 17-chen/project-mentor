#!/usr/bin/env python3
"""Create a secret-safe, read-only inventory for Project Mentor."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


IGNORED_DIRS = {
    ".git", ".hg", ".svn", ".next", ".nuxt", ".svelte-kit", ".turbo",
    ".venv", "venv", "env", "node_modules", "vendor", "dist", "build",
    "coverage", "target", "out", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".cache", ".idea", ".vscode",
}
SENSITIVE_NAMES = {
    ".env", ".npmrc", ".pypirc", "credentials", "credentials.json",
    "secrets.json", "service-account.json", "id_rsa", "id_ed25519",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore"}
GENERATED_SUFFIXES = {".map", ".min.js", ".min.css", ".pyc", ".class", ".o"}
BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
    ".gz", ".tar", ".mp3", ".mp4", ".mov", ".woff", ".woff2", ".ttf",
    ".sqlite", ".db",
}
KEY_FILES = {
    "README.md", "PROJECT_CONTEXT.md", "ARCHITECTURE.md", "DECISION_LOG.md",
    "TODO.md", "CHANGELOG.md", "package.json", "pnpm-workspace.yaml", "yarn.lock",
    "pnpm-lock.yaml", "package-lock.json", "pyproject.toml", "requirements.txt",
    "Pipfile", "poetry.lock", "uv.lock", "Cargo.toml", "go.mod", "Gemfile",
    "docker-compose.yml", "docker-compose.yaml", "Dockerfile", "netlify.toml",
    "vercel.json", "render.yaml", "fly.toml", "Procfile", "Makefile",
}
LANGUAGE_BY_SUFFIX = {
    ".ts": "TypeScript", ".tsx": "TypeScript/React", ".js": "JavaScript",
    ".jsx": "JavaScript/React", ".py": "Python", ".rs": "Rust", ".go": "Go",
    ".java": "Java", ".kt": "Kotlin", ".swift": "Swift", ".rb": "Ruby",
    ".php": "PHP", ".cs": "C#", ".c": "C", ".cpp": "C++", ".h": "C/C++",
    ".vue": "Vue", ".svelte": "Svelte", ".html": "HTML", ".css": "CSS",
    ".scss": "SCSS", ".sql": "SQL", ".sh": "Shell", ".md": "Markdown",
}


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_sensitive(path: Path) -> bool:
    name = path.name.lower()
    if name in SENSITIVE_NAMES or path.suffix.lower() in SENSITIVE_SUFFIXES:
        return True
    if name.startswith(".env") and name not in {".env.example", ".env.sample", ".env.template"}:
        return True
    return any(part.lower() in {"secrets", ".secrets"} for part in path.parts)


def classify(path: Path) -> str:
    if is_sensitive(path):
        return "sensitive"
    lower = path.name.lower()
    if path.suffix.lower() in BINARY_SUFFIXES:
        return "binary"
    if any(lower.endswith(suffix) for suffix in GENERATED_SUFFIXES):
        return "generated"
    return "source"


def run_git(root: Path, args: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True,
            timeout=10, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "error": type(exc).__name__}
    if result.returncode != 0:
        return {"ok": False, "error": result.stderr.strip()[:300]}
    return {"ok": True, "output": result.stdout.rstrip()}


def git_inventory(root: Path, log_limit: int) -> dict[str, Any]:
    inside = run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if not inside.get("ok") or inside.get("output") != "true":
        return {"available": False}

    status = run_git(root, ["status", "--short"])
    branch = run_git(root, ["branch", "--show-current"])
    shallow = run_git(root, ["rev-parse", "--is-shallow-repository"])
    log = run_git(root, ["log", f"-{log_limit}", "--date=short", "--pretty=format:%h%x09%ad%x09%s"])
    changes = status.get("output", "").splitlines() if status.get("ok") else []
    commits = []
    if log.get("ok"):
        for line in log.get("output", "").splitlines():
            parts = line.split("\t", 2)
            if len(parts) == 3:
                commits.append({"hash": parts[0], "date": parts[1], "subject": parts[2]})
    return {
        "available": True,
        "branch": branch.get("output") if branch.get("ok") else None,
        "is_shallow": shallow.get("output") == "true" if shallow.get("ok") else None,
        "working_tree_changes": changes,
        "recent_commits": commits,
    }


def inventory(root: Path, max_files: int, log_limit: int) -> dict[str, Any]:
    files: list[str] = []
    key_files: list[str] = []
    sensitive_paths: list[str] = []
    binary_count = 0
    generated_count = 0
    ignored_directories: Counter[str] = Counter()
    languages: Counter[str] = Counter()
    truncated = False

    for current, dirs, names in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        kept_dirs = []
        for dirname in sorted(dirs):
            if dirname in IGNORED_DIRS:
                ignored_directories[dirname] += 1
            else:
                kept_dirs.append(dirname)
        dirs[:] = kept_dirs

        for name in sorted(names):
            path = current_path / name
            rel = relative(path, root)
            category = classify(path)
            if category == "sensitive":
                sensitive_paths.append(rel)
                continue
            if category == "binary":
                binary_count += 1
                continue
            if category == "generated":
                generated_count += 1
                continue
            files.append(rel)
            if name in KEY_FILES or name.startswith("Dockerfile"):
                key_files.append(rel)
            language = LANGUAGE_BY_SUFFIX.get(path.suffix.lower())
            if language:
                languages[language] += 1
            if len(files) >= max_files:
                truncated = True
                dirs[:] = []
                break
        if truncated:
            break

    return {
        "schema_version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "read_only": True,
        "scan": {
            "max_files": max_files,
            "truncated": truncated,
            "included_file_count": len(files),
            "excluded_sensitive_count": len(sensitive_paths),
            "excluded_binary_count": binary_count,
            "excluded_generated_count": generated_count,
            "ignored_directories": dict(sorted(ignored_directories.items())),
        },
        "languages_by_file_count": dict(languages.most_common()),
        "key_files": sorted(key_files),
        "files": files,
        "sensitive_paths_redacted": sorted(sensitive_paths),
        "git": git_inventory(root, log_limit),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Project root to inventory")
    parser.add_argument("--max-files", type=int, default=5000)
    parser.add_argument("--git-log-limit", type=int, default=30)
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Project root is not a directory: {root}")
    if args.max_files < 1 or args.git_log_limit < 0:
        raise SystemExit("Limits must be non-negative and max-files must be at least 1")
    payload = inventory(root, args.max_files, args.git_log_limit)
    print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
