# 技术栈识别规则

技术是否“正在使用”应由多种证据共同确认。优先级从高到低为：运行入口或调用、源码 import、框架配置、直接依赖、锁文件、命名或目录惯例。

## 前端

- React：直接依赖加 `createRoot`、JSX/TSX 或框架入口。
- Next.js：`next` 直接依赖、Next 配置以及 `app/` 或 `pages/` 路由入口。
- Vue/Nuxt：直接依赖、`createApp` 或 Nuxt 配置与页面入口。
- Svelte/SvelteKit：直接依赖、Svelte 配置和路由文件。
- Vite：Vite 配置或启动脚本只证明构建工具，不自动证明 UI 框架。

区分 UI 框架、路由、状态管理、样式系统、构建工具和测试工具。

## 后端与 API

- Python：结合 `pyproject.toml`/requirements、应用入口和 import 判断 FastAPI、Django 或 Flask。
- Node.js：结合启动脚本、路由注册和服务入口判断 Express、Fastify、NestJS 或框架内 API。
- Serverless/Edge：必须有平台配置、函数目录或部署声明，不要仅根据无服务器风格函数推断。

识别 API 协议、路由边界、服务层、后台任务和异步队列时，沿真实调用链确认。

## 数据与状态

区分：

- 主数据库
- ORM 或查询构建器
- migration 工具
- 缓存
- 对象存储
- 浏览器或进程内状态

存在数据库 SDK 不代表生产正在使用该数据库。优先寻找模型、查询、migration 和配置变量名的组合证据。

## AI 能力

分别识别：

- 模型提供商与 SDK
- 模型名（仅在配置或调用中明确时）
- 提示词的存放与构造
- 流式或非流式响应
- 工具调用、结构化输出或 Agent 循环
- embeddings、向量库、检索与重排
- 音频、图像或视频处理链

SDK 存在不代表某一具体模型正在运行。环境变量名可证明集成意图，但不能证明生产配置值。

## 测试与质量

区分单元、集成、端到端和手工测试。测试框架依赖不代表存在有效覆盖；读取测试文件、脚本和 CI 执行步骤共同判断。

## 构建与部署

区分本地开发、容器构建、CI 和生产托管。Dockerfile 或 Compose 文件存在只证明提供了该路径；是否用于生产需要部署记录或平台配置。

## 证据输出示例

```text
已确认（高）：前端使用 React。
证据：`package.json` 的直接依赖 `react`；`src/main.tsx` 调用 `createRoot`。

合理推断（中）：Vite 被选作轻量开发构建工具。
证据：`vite.config.ts` 与 `package.json` 的 `dev` 脚本。
限制：仓库未记录原始选型原因。
```
