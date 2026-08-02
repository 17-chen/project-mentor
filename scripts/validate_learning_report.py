#!/usr/bin/env python3
"""Validate the structure and basic evidence hygiene of a learning report."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED = {
    "阅读说明.md": ["学习", "范围"],
    "架构地图.md": ["架构"],
    "技术栈教学.md": ["技术"],
    "工程过程复盘.md": ["工程"],
    "术语表.md": ["术语"],
    "风险与工程经验.md": ["风险"],
    "面试问题.md": ["问题", "参考回答"],
}
PLACEHOLDERS = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?(?:TODO|TBD|FIXME)(?:\s*[:：].*)?$|\{\{[^}]+\}\}|<待[^>]*>"
)
MARKDOWN_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def validate(learning_dir: Path) -> list[str]:
    errors: list[str] = []
    texts: dict[str, str] = {}

    course_path = learning_dir / "工程学习课程.md"
    if course_path.is_file():
        text = course_path.read_text(encoding="utf-8")
        if len(text.strip()) < 800:
            errors.append("单文件课程内容过短：工程学习课程.md")
        if PLACEHOLDERS.search(text):
            errors.append("存在未替换占位符：工程学习课程.md")
        for keyword in ("学习", "工作", "技术", "下一步"):
            if keyword not in text:
                errors.append(f"单文件课程缺少关键内容“{keyword}”：工程学习课程.md")
        if "<details>" in text or "<summary>" in text:
            errors.append("工程学习课程.md 使用了预览不兼容的 HTML 折叠标签")
        if text.count("```mermaid") > text.count("```") - text.count("```mermaid"):
            errors.append("Mermaid 代码块可能未闭合：工程学习课程.md")
        return errors

    for name, keywords in REQUIRED.items():
        path = learning_dir / name
        if not path.is_file():
            errors.append(f"缺少文件：{name}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        if len(text.strip()) < 120:
            errors.append(f"内容过短：{name}")
        if PLACEHOLDERS.search(text):
            errors.append(f"存在未替换占位符：{name}")
        for keyword in keywords:
            if keyword not in text:
                errors.append(f"缺少关键内容“{keyword}”：{name}")
        if text.count("```mermaid") > text.count("```") - text.count("```mermaid"):
            errors.append(f"Mermaid 代码块可能未闭合：{name}")

    for name, text in texts.items():
        for target in MARKDOWN_LINK.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean = target.strip("<>").split("#", 1)[0]
            candidate = Path(clean) if Path(clean).is_absolute() else learning_dir / clean
            if clean and not candidate.resolve().exists():
                errors.append(f"失效的相对链接：{name} -> {target}")

    all_text = "\n".join(texts.values())
    secret_patterns = [
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"(?i)(?:api[_-]?key|secret|password)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}",
    ]
    if any(re.search(pattern, all_text) for pattern in secret_patterns):
        errors.append("报告疑似包含秘密值")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("learning_dir", type=Path)
    args = parser.parse_args()
    learning_dir = args.learning_dir.expanduser().resolve()
    if not learning_dir.is_dir():
        print(f"验证失败：目录不存在：{learning_dir}")
        return 2
    errors = validate(learning_dir)
    if errors:
        print("学习报告验证失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print("学习报告结构验证通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
