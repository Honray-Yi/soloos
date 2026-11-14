# SoloOS 仓库导航 / Repository map

先选使用方式：**只想复制提示词**，从 [prompt-edition](prompt-edition/README.md) 开始；**需要程序校验、计算和记录**，从 [README](README.md) 的完整版本开始。

## 三个入口，职责分开

| 位置 | 面向谁 | 应在哪里修改 |
| --- | --- | --- |
| [prompt-edition/](prompt-edition/README.md) | 想在普通 AI 对话里使用、编辑角色守则的个人 | 直接编辑提示词或个性化覆盖文件 |
| [.agents/skills/soloos/](.agents/skills/soloos/SKILL.md) | 使用 Codex standalone Skill 或开发运行时的人 | 这是完整运行时的唯一源文件目录 |
| [plugins/soloos/](plugins/soloos/plugin.json) | 需要安装便携插件的用户 | 自动生成，不单独修改其中的副本 |

完整 Skill 和插件里的重复代码是有意的：源文件与分发副本必须一致，CI 会检查。简易版是独立的文字工作流，不声称拥有完整版本的代码校验、存储或权限保障。

## 其他目录

| 位置 | 内容 |
| --- | --- |
| `.agents/plugins/` | 本地私有插件目录的入口配置 |
| [packaging/](packaging/README.md) | 插件清单、目录配置源、官方 schema；不含密钥 |
| `tests/` | 计算、数据、报告、权限、存储、并发与打包回归测试 |
| `tools/` | 开发辅助：构建 schema、虚构样本、安装、打包和仓库检查 |
| [examples/](examples/README.md) | 完整版虚构输入与生成结果；不是用户真实业务数据 |
| `.github/` | Windows/Linux CI、issue 和 PR 模板 |

本地 `work/`、`dist/`、`.venv/`、测试缓存、SQLite 文件和 `.env` 被 Git 排除；它们不应出现在上传文件清单中。私有仓库同样不应存放真实客户数据、令牌或审批日志。

## 根目录文档

- [README.md](README.md)：产品入口、运行方式和示例。
- [DEPLOYMENT.md](DEPLOYMENT.md)：Skill/插件安装和已验证的兼容性边界。
- [PRD.md](PRD.md)、[ARCHITECTURE.md](ARCHITECTURE.md)：需求与架构。
- [ROADMAP.md](ROADMAP.md)、[PLAN.md](PLAN.md)：交付状态；PLAN 中旧阶段记录明确标为历史。
- [QA.md](QA.md)：实际测试证据、缺陷与未执行的验收检查。
- [CHANGELOG.md](CHANGELOG.md)：版本变化。
- [CONTRIBUTING.md](CONTRIBUTING.md)、[SECURITY.md](SECURITY.md)：修改和安全要求。
- [AGENTS.md](AGENTS.md)：开发助手应遵守的项目规则。

仓库继续保持私有，不添加开源许可证。公开分享、业务执行和服务部署需要另外授权。
