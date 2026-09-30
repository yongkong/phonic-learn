# AGENTS.md

> **语言约定**：本项目所有输出内容一律使用中文书写，包括文档、Issue 正文、说明与设计文字，以及 Matt Pocock 技能相关文档（本文件的 Agent skills 部分与 `docs/agents/*.md`）。命令、代码、API 名称、标签字符串等保持英文原样。

## Agent skills

### Issue tracker

Issue 跟踪在 GitHub Issues（`yongkong/phonic-learn`），通过 `gh` CLI 管理。见 `docs/agents/issue-tracker.md`。

### Triage labels

五个标准 triage 角色，使用默认标签字符串（`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`）。见 `docs/agents/triage-labels.md`。

### Domain docs

单上下文（single-context）：仓库根目录一个 `CONTEXT.md` + `docs/adr/`。见 `docs/agents/domain.md`。
