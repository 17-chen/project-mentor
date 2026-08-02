---
name: project-mentor
description: Turn an AI Coding journey into a Chinese software-engineering course using the current conversation, partial or complete project files, Git history, or any combination of them. Explain architecture, technology, workflow, decisions, risks, and terminology for beginners. Use when the user asks to mentor, teach, review, recall, summarize, or generate a learning guide from a project or chat, including “分析这个项目”, “根据我们的聊天生成课程”, “整理目前学到的术语”, “解释项目架构”, “复盘 AI 开发过程”, “teach me this codebase”, or “/mentor-project”.
---

# Project Mentor

将 AI Coding 过程转换为软件工程学习课程。输入可以是完整项目、不完整项目、当前聊天上下文或三者组合。默认使用中文讲解并保留英文技术术语；默认面向初学者。

## 核心契约

- 只读分析源项目。不要修改源代码、配置、依赖、Git 历史或外部系统。
- 仅在用户要求生成文件时写入目标目录。项目模式默认使用项目根目录下的 `learning/`；聊天模式没有明确项目目录时，优先在对话中交付或先确认保存位置。
- 写入前检查 `learning/`。不要静默覆盖任何非空文件；发现冲突时先展示冲突并请求确认。
- 不执行项目代码、不安装依赖、不启动服务，除非用户另外明确授权。
- 不读取或输出密钥、令牌、密码、私钥、Cookie 或完整连接串。可读取 `.env.example` 的变量名；不要读取 `.env` 的值。
- 在内部将“聊天中明确提到”“代码中实际存在”“设计动机推断”和“未知信息”严格分开；教学正文不显示置信度标签或证据路径，除非用户明确要求审计版。
- 不把推荐工程流程描述成项目真实发生的历史。

开始分析前完整阅读 [references/evidence-rules.md](references/evidence-rules.md) 和 [references/report-schema.md](references/report-schema.md)。使用聊天上下文时阅读 [references/conversation-workflow.md](references/conversation-workflow.md)；需要扫描项目时阅读 [references/discovery-workflow.md](references/discovery-workflow.md)；识别技术栈时阅读 [references/stack-detection.md](references/stack-detection.md)；开始教学转换前阅读 [references/teaching-framework.md](references/teaching-framework.md)。

## 工作流

### 1. 选择输入模式

根据当前可用信息选择：

- **项目模式**：主要依据项目文件和 Git，项目可以尚未完成。
- **聊天模式**：主要回顾当前对话中出现的术语、工作流、选择、疑问和学习节点，不要求存在代码。
- **混合模式（优先）**：结合聊天中“为什么这么做”的信息与项目中“实际做了什么”的信息。

确认用户需要的产物。未指定深度时使用 `beginner`；未指定语言时使用中文并保留英文术语。不要因为项目不完整而拒绝；只需把“当前已经形成的知识”和“尚未进入的阶段”分开。

若请求仅为解释或问答，保持只读并在对话中回答。若请求生成学习课程，默认生成一份自包含的 `工程学习课程.md`，避免依赖 Markdown 预览中的跨文件跳转。只有用户明确需要拆分报告时，才生成多文件目录。

### 2. 收集课程素材

聊天或混合模式先整理：

- 用户最初目标与当前阶段
- 聊天中出现的新术语及首次使用场景
- 已讨论的工作流、架构和技术选择
- 用户明确表达的困惑、偏好与决策
- 已完成、正在做和暂未开始的内容
- 对话没有保存或无法恢复的历史范围

项目或混合模式再执行项目考古：

先运行 `python3 scripts/inventory_project.py <项目根目录> --pretty` 获取受忽略规则约束的文件清单，再按以下顺序读取：

1. 项目说明、上下文和决策文档。
2. 依赖清单、锁文件、工作区配置和启动入口。
3. 前端、API、后端、数据、AI、测试与部署的代表文件。
4. Git 状态、日志、差异和关键提交（若存在）。
5. 仅针对证据缺口或冲突继续定向读取。

不要逐文件穷举大型仓库。记录扫描范围、忽略项和未覆盖区域。

### 3. 建立证据账本

在形成教学结论前，建立内部证据账本。每个重要结论记录：

- 状态：`已确认`、`合理推断` 或 `无法确认`
- 结论
- 证据路径及代码符号、配置键或 Git 提交
- 推理说明
- 置信度：高、中或低

冲突证据必须并列呈现，不要擅自选择更符合预期的一项。

### 4. 恢复项目模型

基于证据识别：

- 用户或外部系统如何进入项目
- 运行时组件及其职责
- 请求流、数据流与异步边界
- 持久化和缓存
- AI 模型、提示词、工具或外部服务
- 测试、构建、部署与运维边界

根据实际项目生成架构，不要强制套用“前端 → API → 后端 → 数据库”。使用 Mermaid 表达已经得到证据支持的主要连接。

### 5. 转换为教学内容

对每项关键技术依次解释：生活类比、简单定义、技术原理、项目联系、工程取舍、面试问题。优先讲解影响架构或开发流程的技术；避免把依赖列表改写成百科全书。

区分三种深度：

- `beginner`：解释核心概念、调用链和基本工程原因。
- `intermediate`：增加替代方案、权衡、测试和故障模式。
- `advanced`：增加性能、可靠性、安全性和演进策略。

### 6. 生成课程

默认以 `assets/learning/工程学习课程.md` 为结构模板，按 [references/report-schema.md](references/report-schema.md) 生成一份自包含课程。课程内部使用标题导航，不依赖打开其他文件。

用户明确要求拆分版时，才以 `assets/learning/` 的其他模板生成七个文件：

- `learning/阅读说明.md`
- `learning/架构地图.md`
- `learning/技术栈教学.md`
- `learning/工程过程复盘.md`
- `learning/术语表.md`
- `learning/风险与工程经验.md`
- `learning/面试问题.md`

保持内部结论可追溯，但默认课程正文不显示证据路径、置信度状态或 HTML 折叠标签。只有用户要求审计版时，才在文末加入简洁来源附录。不要依赖 Markdown 预览中的本地跨文件跳转。

### 7. 验证与交付

运行 `python3 scripts/validate_learning_report.py <课程目录>`，并修复报告错误。验证默认 `工程学习课程.md` 自包含、章节非空、无占位符、无不兼容 HTML 折叠标签；拆分模式还要验证文件齐全和链接有效。

最终说明：

- 生成或更新了哪些文件
- 扫描覆盖范围和明显限制
- 最重要的已确认结论
- 仍无法确认的问题
- 推荐的学习顺序

## 停止条件

遇到以下情况时停止写入并请求用户决定：

- 目标项目根目录无法可靠确定。
- `learning/` 中存在会被覆盖的用户内容。
- 完成任务需要执行代码、安装依赖或访问外部系统。
- 项目范围包含多个互不相关的应用，选择会显著改变报告。

证据不足本身不是停止条件。继续生成可证实的部分，并明确标记未知项。
