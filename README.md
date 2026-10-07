# Voice Task Router

一个面向 Codex 的 skill，帮助你把语音或文字中的想法整理成清楚、可执行的需求，并在后续对话里持续维护同一份需求草稿。

## 它做什么

- 先判断用户要讨论什么，再决定是否需要澄清；只追问会改变任务方向的关键缺口。
- 把补充和修正并入现有需求，保留仍然兼容的约束。
- 输出可以直接交给工作对话执行的完整提示词，并给出具体模型和推理强度建议。
- 用户说“下一步”时，先读取关联项目的最新进度，再推荐值得推进的工作。
- 先保证任务完整、质量和完成效率，再比较整个任务的综合成本。

默认角色是需求讨论伙伴。它不会因为用户说“继续”“实现”或“下一步”就擅自修改项目、运行任务、生成素材或派发代理。用户明确要求在当前对话执行，或直接维护本 skill 时，才按相应请求切换。

## 安装与使用

把整个 `voice-task-router` 目录放进 Codex 的 skills 目录，例如：

```text
$CODEX_HOME/skills/voice-task-router/
```

在新需求的消息开头明确调用 `$voice-task-router`，并附上你想讨论的目标。随后可以在同一对话里补充、纠正或说“下一步”；本 skill 会继续维护同一份需求。需要交给执行对话时，它会提供完整提示词、模型名和推理强度。

用户可以直接要求“退出需求讨论模式”。如果需要手动改状态，可用当前对话的真实 UUID 调用辅助脚本：

```powershell
python -X utf8 "$env:CODEX_HOME\skills\voice-task-router\scripts\session_mode.py" status --session-id "<当前 Codex 对话 UUID>"
python -X utf8 "$env:CODEX_HOME\skills\voice-task-router\scripts\session_mode.py" deactivate --session-id "<当前 Codex 对话 UUID>"
```

脚本要求真实 UUID；不能用示例值或关联项目对话的 UUID 代替当前对话 ID。也可以用 `activate` 手动登记当前对话。

## 工作原理

1. `SKILL.md` 规定角色、需求整理流程、模型推荐原则和草稿交付格式。
2. `references/` 提供更细的需求澄清、口述重建、模型路由、协作分工和状态恢复说明。
3. 可选的 Codex 原生 Hook 把事件 JSON 传给 `scripts/session_mode.py hook`。脚本只接受 `UserPromptSubmit` 和 `SessionStart` 事件，并只在当前用户消息明确调用 skill 时登记启用。
4. 后续 Hook 事件按当前对话 UUID 恢复模式提醒。脚本不扫描聊天历史，也不把项目链接里的 UUID 当成当前对话 ID。
5. 每个对话的状态以原子文件替换方式写入 Codex 根目录下的 `state/voice-task-router/<对话 UUID>.json`。文件只记录 UUID、启用状态、来源和更新时间，不保存需求正文或聊天内容。

Hook 必须由用户在 Codex 环境中单独配置并信任。本仓库提供状态脚本和技能文件，不会自动改写 Codex 设置或安装 Hook。Hook 的事件格式和配置方式请以对应版本的 [Codex Hooks 文档](https://learn.chatgpt.com/docs/hooks) 为准。

## 文件结构

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 主工作流程与行为边界 |
| `agents/openai.yaml` | 技能展示名称、描述和默认调用提示 |
| `references/requirements-dialogue.md` | 连续需求讨论与下一步选择 |
| `references/voice-prompting.md` | 将口述意图整理成执行提示词 |
| `references/model-routing.md` | 模型、推理强度、速度和综合成本的选择原则 |
| `references/benchmark-evidence.md` | 带日期的模型和计费证据快照 |
| `references/hybrid-delegation.md` | 评估是否采用 Sol/Astra 主持与 Luna 子任务 |
| `references/session-persistence.md` | Hook、状态登记、恢复与核验边界 |
| `references/active-project.md` | 用户本地填写的活动项目对话指针模板 |
| `scripts/session_mode.py` | Hook 事件解析与每对话状态辅助脚本 |

## 边界与隐私

- 仅在当前对话明确调用时启用；引用、代码块或聊天标题中的调用文本不会单独启用它。
- 状态文件不含需求内容。草稿正文仍在 Codex 对话上下文中；状态文件本身不能恢复已丢失的聊天历史。
- 自动恢复依赖 Hook 已安装、受信任且能收到正确事件。脚本失败会报告问题，不会假装登记成功。
- 项目进度需要通过当前可用的对话或项目读取能力核实。读不到时，应说明缺口，不能把旧摘要说成最新状态。
- 模型与计费材料是注明日期的参考快照，不保证永久反映当前产品选项；使用前应按用户实际可选设置核对。

## License

MIT，详见 [LICENSE](LICENSE)。

---

### English summary

Voice Task Router is a Codex skill for ongoing requirement clarification. It keeps one evolving brief, turns confirmed intent into a copy-ready execution prompt, and recommends a model and reasoning effort. Optional native Hooks can persist a minimal per-conversation active flag; they must be configured separately. The skill is a discussion and routing workflow by default, not an automatic project executor. See the Chinese sections above for installation, usage, architecture, privacy, and limitations.
