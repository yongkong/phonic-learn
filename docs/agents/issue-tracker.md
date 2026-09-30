# Issue 跟踪：GitHub

本仓库的 issue 与规格文档以 GitHub issue 形式管理，所有操作使用 `gh` CLI。

## 约定

- **创建 issue**：`gh issue create --title "..." --body "..."`。多行正文使用 heredoc。
- **读取 issue**：`gh issue view <number> --comments`，用 `jq` 过滤评论并同时获取标签。
- **列出 issue**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，按需配合 `--label` 与 `--state` 过滤。
- **评论**：`gh issue comment <number> --body "..."`
- **添加 / 移除标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**：`gh issue close <number> --comment "..."`

仓库从 `git remote -v` 推断；在 clone 内运行 `gh` 时会自动识别。

## Pull request 作为 triage 面

**PR 作为请求面：否。**（如果本仓库要把外部 PR 当作功能请求处理，改为 `yes`；`/triage` 会读取此开关。）

设为 `yes` 时，PR 与 issue 使用相同的标签与状态，改用对应的 `gh pr` 命令：

- **读取 PR**：`gh pr view <number> --comments`；`gh pr diff <number>` 查看差异。
- **列出待 triage 的外部 PR**：`gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`，只保留 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的（丢弃 `OWNER`/`MEMBER`/`COLLABORATOR`）。
- **评论 / 打标签 / 关闭**：`gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`。

GitHub 的 issue 与 PR 共用同一编号空间，单独一个 `#42` 可能是两者之一：先用 `gh pr view 42` 解析，失败再回退到 `gh issue view 42`。

## 当技能说"发布到 issue 跟踪器"

创建一个 GitHub issue。

## 当技能说"获取相关工单"

运行 `gh issue view <number> --comments`。

## Wayfinding 操作

供 `/wayfinder` 使用。**地图（map）**是一个单独的 issue，**子（child）** issue 作为工单。

- **地图**：一个标记 `wayfinder:map` 的单独 issue，正文承载 Notes / Decisions-so-far / Fog。`gh issue create --label wayfinder:map`。
- **子工单**：作为 GitHub sub-issue 关联到地图（对 sub-issues 端点调用 `gh api`）。若 sub-issues 未启用，则把子工单加进地图正文的任务列表，并在子工单正文顶部写上 `Part of #<map>`。标签：`wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）。认领后，工单指派给驱动的开发者。
- **阻塞关系**：使用 GitHub **原生 issue 依赖**（issue dependencies），这是规范且在 UI 中可见的表示方式。添加一条边：`gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`，其中 `<blocker-db-id>` 是阻塞方的数字 **数据库 id**（`gh api repos/<owner>/<repo>/issues/<n> --jq .id`，不是 `#number`，也不是 `node_id`）。GitHub 通过 `issue_dependencies_summary.blocked_by` 上报（仅统计未关闭的阻塞方，即实时门槛）。若依赖功能不可用，回退为在子工单正文顶部写一行 `Blocked by: #<n>, #<n>`。所有阻塞方都关闭后，工单即解除阻塞。
- **前沿查询（frontier query）**：列出地图的未关闭子工单（`gh issue list --state open`，限定在地图的 sub-issues / 任务列表范围内），剔除任何有未关闭阻塞方（`issue_dependencies_summary.blocked_by > 0`，或 `Blocked by` 行中存在未关闭 issue）或已有指派者的；按地图顺序取第一个。
- **认领**：`gh issue edit <n> --add-assignee @me`，这是会话的第一个写操作。
- **解决**：`gh issue comment <n> --body "<answer>"`，然后 `gh issue close <n>`，最后向地图的 Decisions-so-far 追加上下文指针（gist + 链接）。
