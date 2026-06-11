# Agent Collaboration Workflow

一个给 Codex、Claude、Cursor 和其他 AI coding agent 共用的协作上下文工作流。

这个仓库不是业务项目本身，而是一个可以安装到其他代码仓库里的“协作协议模板”。安装后，不同 AI 工具和真人开发者可以通过同一组文件理解任务背景、当前进度、交接状态和 PR 审查重点。

## 给真人看

### 这个仓库是干什么的

当一个任务被多个 AI 工具、多个会话或多个人连续处理时，最容易丢失的是上下文：

- 这个任务到底要解决什么问题
- 哪些事情不在范围内
- 做过哪些决定
- 哪些假设后来变了
- 运行过哪些测试或验证
- 现在卡在哪里
- 下一个人或下一个 agent 应该从哪里继续

这个仓库提供一套文件化的协作规范，把这些信息固定在目标项目里，而不是只留在聊天记录里。

安装后，目标项目会获得：

```text
AGENTS.md
CLAUDE.md
.cursor/rules/agent-collaboration.mdc
.agents/skills/agent-collaboration/SKILL.md
docs/ai-collaboration-sop.md
docs/templates/context-pack.md
docs/templates/handoff.md
docs/templates/pr-context-diff.md
tools/agent-context.py
```

核心文件含义：

- `Context Pack`：任务长期上下文，记录目标、非目标、假设、约束、决策、验证证据和风险。
- `Handoff`：交接文件，记录当前进度、改了什么、跑了什么验证、还有什么阻塞。
- `PR Context Diff`：给 reviewer 看的变更上下文，说明从初始任务到最终实现之间发生了哪些关键变化。
- `tools/agent-context.py`：命令行工具，用来创建任务文件和检查上下文是否完整。

### 一键安装到目标项目

先 clone 这个仓库：

```bash
git clone https://github.com/YOUR_ORG/agent-collaboration-workflow.git
```

进入你真正要接入协作协议的项目：

```bash
cd /path/to/your/project
/path/to/agent-collaboration-workflow/install.sh
```

也可以显式指定目标项目路径：

```bash
/path/to/agent-collaboration-workflow/install.sh /path/to/your/project
```

安装脚本不会直接覆盖已有的 `AGENTS.md` 和 `CLAUDE.md`。如果这些文件已经存在，它会追加一个受控区块；其他协作模板和工具文件会在缺失时创建。

### 创建一个任务上下文

在目标项目里运行：

```bash
python3 tools/agent-context.py scaffold TASK-123 \
  --title "Short task title" \
  --owner "Owner or team" \
  --source "Issue, PR, ticket, or conversation link"
```

这会创建：

```text
docs/tasks/TASK-123/context-pack.md
docs/tasks/TASK-123/handoff.md
docs/tasks/TASK-123/pr-context-diff.md
```

### 检查上下文是否完整

普通结构检查：

```bash
python3 tools/agent-context.py check TASK-123
```

严格检查全部任务：

```bash
python3 tools/agent-context.py check-all --strict
```

`--strict` 会在这些情况失败：

- 必要文件缺失
- 必要标题缺失
- 模板里的 `TODO(...)`、`TBD`、`FIXME` 等占位符还没填

### 推荐使用流程

1. 把这个仓库安装到目标项目。
2. 为每个重要任务创建一个 `docs/tasks/<task-id>/`。
3. 开始工作前读 `context-pack.md`。
4. 任务理解发生变化时更新 `context-pack.md`。
5. 停止工作前更新 `handoff.md`。
6. 提 PR 前更新 `pr-context-diff.md`。
7. 交接或 review 前运行 `python3 tools/agent-context.py check-all --strict`。

### GitHub Actions

仓库包含：

```text
.github/workflows/context-check.yml
```

它会在 PR 或手动触发时运行安装和 CLI 冒烟测试。如果目标项目存在 `docs/tasks`，还会执行严格上下文检查。

## 给 AI Agent 看

### 你的目标

你是被要求配置或使用 Agent Collaboration Workflow 的 AI coding agent。下载本仓库后，你需要把它安装到用户指定的目标项目中，并确保 Codex、Claude、Cursor 和通用 agent 都能通过文件读取协作上下文。

不要只解释概念。优先完成实际配置。

### 安装步骤

1. 确认当前仓库是本模板仓库，里面应该存在：

   ```text
   install.sh
   tools/agent-context.py
   docs/templates/context-pack.md
   docs/templates/handoff.md
   docs/templates/pr-context-diff.md
   ```

2. 确认用户要接入的目标项目路径。如果用户已经在目标项目目录内，则使用当前目录作为目标路径。

3. 从模板仓库运行安装脚本：

   ```bash
   ./install.sh /path/to/target/project
   ```

   如果当前目录就是目标项目，且模板仓库在其他路径：

   ```bash
   /path/to/agent-collaboration-workflow/install.sh
   ```

4. 安装完成后，在目标项目里检查这些文件是否存在：

   ```text
   AGENTS.md
   CLAUDE.md
   .cursor/rules/agent-collaboration.mdc
   .agents/skills/agent-collaboration/SKILL.md
   docs/ai-collaboration-sop.md
   docs/templates/context-pack.md
   docs/templates/handoff.md
   docs/templates/pr-context-diff.md
   tools/agent-context.py
   ```

5. 如果用户提供了任务 ID，创建任务上下文：

   ```bash
   python3 tools/agent-context.py scaffold <task-id> \
     --title "<short title>" \
     --owner "<owner>" \
     --source "<issue, PR, ticket, or conversation link>"
   ```

6. 如果用户没有提供任务 ID，不要编造正式 ID。可以建议一个临时 ID，例如 `TASK-001`，并请用户确认。

### 配置后要验证

在目标项目里运行：

```bash
python3 tools/agent-context.py --help
python3 tools/agent-context.py status
```

如果已经创建了任务：

```bash
python3 tools/agent-context.py check <task-id>
```

严格检查：

```bash
python3 tools/agent-context.py check-all --strict
```

注意：刚 scaffold 出来的任务通常会因为模板中的 `TODO(...)` 在严格检查里失败。这是正常的。你应该向用户说明哪些占位内容还需要补齐，而不是把占位内容随便编完整。

### Agent 使用规则

每次处理已接入此工作流的目标项目时：

1. 先读 `AGENTS.md`。
2. 再读 `docs/ai-collaboration-sop.md`。
3. 识别当前任务 ID。
4. 如果存在，读取：

   ```text
   docs/tasks/<task-id>/context-pack.md
   docs/tasks/<task-id>/handoff.md
   docs/tasks/<task-id>/pr-context-diff.md
   ```

5. 开发过程中，如果目标、假设、约束、决策、验证证据或风险发生变化，更新 `context-pack.md`。
6. 停止工作前，更新 `handoff.md`。
7. 准备 PR 前，更新 `pr-context-diff.md`。
8. 不要编造产品意图、验证结果、决策、审批或用户确认。未知内容保留为明确的 `TODO(<owner>): ...`。

### Codex 自动化 Prompt

只读项目健康检查：

```text
Use $agent-collaboration.

Audit this project's agent collaboration context health.

Steps:
1. Read AGENTS.md and docs/ai-collaboration-sop.md if present.
2. Run `python3 tools/agent-context.py check-all --strict`.
3. If the command passes, report a short summary with the number of checked task context packs.
4. If the command fails, report each missing file, missing heading, placeholder, or escalated-task requirement exactly enough for a human or agent to fix it.
5. Do not modify files during this automation run unless the user explicitly asks for autofix.

Output format:
- Status: Pass / Fail
- Checked tasks:
- Findings:
- Recommended next action:
```

当前线程 heartbeat：

```text
Use $agent-collaboration.

Continue the current agent collaboration workflow in this thread.

Each time this thread wakes up:
1. Identify the active task id from the thread context, branch name, issue link, or existing docs/tasks directory.
2. Read the task Context Pack and handoff if they exist.
3. Check whether recent work changed goals, assumptions, constraints, decisions, validation evidence, or known risks.
4. If the task is ready for review, ensure PR context diff content is prepared.
5. If context artifacts are missing or still contain placeholders, report the exact missing sections and ask for the minimum input needed.
6. Stop or ask for user input when no safe next action is available.

Output format:
- Current task:
- Context status:
- Work since last check:
- Missing information:
- Recommended next step:
```

## 仓库结构

```text
.
├── AGENTS.md
├── CLAUDE.md
├── install.sh
├── scripts/
│   └── smoke-test.sh
├── docs/
│   ├── ai-collaboration-sop.md
│   └── templates/
├── skills/
│   └── agent-collaboration/
├── .agents/
│   └── skills/
├── .cursor/
│   └── rules/
└── tools/
    └── agent-context.py
```

## License

MIT
