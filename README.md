# Project Mentor · AI 工程导师

> Turn AI Coding projects and conversations into practical software-engineering courses.  
> 把 AI Coding 项目与聊天过程转化为适合初学者的软件工程课程。

## 中文介绍

Project Mentor 是一个面向 Codex 的工程教学 Skill。它不仅分析“项目做了什么”，还会把架构、技术栈、开发工作流、工程决策、术语和风险整理成一份可以继续学习的中文课程。

它不要求项目已经完成。你可以使用：

- 完整或未完成的软件项目
- 当前聊天上下文
- 零散代码、规格说明与 Git 历史
- 聊天与项目文件的组合

默认输出一份自包含的 `工程学习课程.md`，避免依赖 Markdown 预览中的跨文件跳转。

## English Overview

Project Mentor is a Codex skill that turns an AI-assisted development journey into a beginner-friendly software-engineering course.

It can work from:

- A complete or incomplete codebase
- The current conversation context
- Partial specifications, source files, and Git history
- A combination of conversation intent and implementation evidence

The default output is a self-contained Chinese course named `工程学习课程.md`. English technical terms are preserved and explained when they first appear.

## What It Teaches · 教学内容

- System architecture and component responsibilities · 系统架构与组件职责
- Frontend, backend, data, AI, and external-service workflows · 前端、后端、数据、AI 与外部服务工作流
- Technology concepts with analogies and project examples · 带生活类比与项目示例的技术概念
- Engineering decisions, alternatives, and trade-offs · 工程决策、替代方案与取舍
- Development process and Git-based reconstruction · 开发过程与 Git 历史复盘
- Risks, unfinished work, and recommended next steps · 风险、未完成内容与下一步
- Exercises and interview questions · 练习题与面试问题

## Three Input Modes · 三种输入模式

### Project Mode · 项目模式

Analyze a complete or partial repository. The skill reads documentation, manifests, representative source files, deployment configuration, tests, and Git history without modifying the source project.

分析完整或未完成的项目，恢复实际架构、调用链和工程过程。

### Conversation Mode · 聊天模式

Turn the current visible conversation into a staged learning guide. No codebase is required.

根据当前聊天中出现的目标、术语、工作流、决策和困惑生成阶段性课程，不要求已经存在代码。

### Hybrid Mode · 混合模式

Combine conversation context—why a choice was discussed—with project evidence—what was actually implemented.

结合聊天中的设计原因与代码中的实际实现。这是信息足够时的优先模式。

## Installation · 安装

Clone the repository into your personal Codex skills directory:

```bash
git clone https://github.com/17-chen/project-mentor.git ~/.agents/skills/project-mentor
```

Codex normally detects local skill changes automatically. If the skill does not appear, restart Codex.

## Usage · 使用方式

Explicit invocation in Codex:

```text
Use $project-mentor to analyze this project and generate a beginner-friendly Chinese engineering course.
```

```text
使用 $project-mentor 回顾当前聊天和项目进度，生成一份适合初学者的单文件工程课程。
```

Other example prompts:

```text
根据我们目前的聊天，整理出现过的技术术语、工作流和工程决策。
```

```text
分析这个尚未完成的项目，告诉我目前已经形成了哪些工程知识。
```

```text
把当前项目转换成课程，并解释如果没有 AI，我应该怎样从零重做。
```

## Default Output · 默认输出

```text
learning/
└── 工程学习课程.md
```

When explicitly requested, the skill can also generate a split course:

```text
learning/
├── 阅读说明.md
├── 架构地图.md
├── 技术栈教学.md
├── 工程过程复盘.md
├── 术语表.md
├── 风险与工程经验.md
└── 面试问题.md
```

## Safety and Accuracy · 安全与准确性

- Keeps source-project analysis read-only by default · 默认只读分析源项目
- Does not run code or install dependencies without authorization · 未经授权不执行代码或安装依赖
- Excludes secrets such as `.env` values and private keys · 排除 `.env` 值与私钥等敏感内容
- Separates implemented facts, conversation plans, inference, and unknowns internally · 内部区分实际实现、聊天计划、推断与未知信息
- Does not present proposed work as completed work · 不把讨论或计划描述成已完成内容

## Repository Structure · 仓库结构

```text
project-mentor/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── learning/
├── references/
│   ├── conversation-workflow.md
│   ├── discovery-workflow.md
│   ├── evidence-rules.md
│   ├── report-schema.md
│   ├── stack-detection.md
│   └── teaching-framework.md
└── scripts/
    ├── inventory_project.py
    └── validate_learning_report.py
```

## Validation · 验证

Validate the skill package:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py /path/to/project-mentor
```

Validate a generated course:

```bash
python3 scripts/validate_learning_report.py /path/to/project/learning
```

## Project Status · 项目状态

Current version: **v0.1**

- Codex skill workflow implemented
- Project, conversation, and hybrid modes implemented
- Chinese single-file and split-course templates implemented
- Secret-safe project inventory implemented
- Course structure validator implemented

The next iteration can focus on broader project testing, incremental course updates, and optional distribution as a Codex plugin.
