# Codex 每个对话的持续模式

## 首次明确调用

原生 `UserPromptSubmit` Hook 从本轮真实 `prompt` 识别明确的 `$voice-task-router` 调用（含 Codex 生成的 Markdown Skill 链接、前置 `codex://threads/...` 项目链接），在模型开始工作前为该事件的 `session_id` 自动登记并注入角色边界和输出契约。前置链接只是项目上下文，不能拿其中的 UUID 代替当前侧栏对话 ID。不从聊天标题、引用、代码块、系统 Skill 目录或历史记录推断激活。不修改项目设置，不执行工作任务。

明确以本 Skill 为对象的维护请求只注入维护提示，不给未启用的对话登记激活。脚本只能识别直接的调用形式和明确维护措辞；语义上仍以用户要求为准。如果本轮实际上仅维护本 Skill，模型须纠正可能的首次误登记；不能把项目或其他 Skill 的维护当成这个例外。已经启用的对话维护后继续原模式。

只有展示调用、没有需求时，说明模式已开启，等待需求。调用附带需求时本轮就讨论或交草稿。

## 补登记和退出

Hook 未加载或不能识别时，本轮依然按 Skill 工作，并补登记。使用**绝对脚本路径**与可用 Python：

```powershell
& 'C:\Users\xiao\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 'C:\Users\xiao\.codex\skills\voice-task-router\scripts\session_mode.py' activate --session-id '<当前真实对话 UUID>'
```

用 `status` 核对状态，用 `deactivate` 退出。真实 UUID 应来自本轮 Hook 上下文或原生当前对话元数据。`CODEX_THREAD_ID` / `CODEX_SESSION_ID` 仅在是有效 UUID 时可用；沙箱中的 `1` 等占位值不是对话 ID。不能猜 ID、使用目标项目 ID或借用其他对话。状态写入用户 Skill 目录之外的 `state/voice-task-router`，如沙箱阻止写入，使用正常授权机制，不通过改其他目录来假装登记成功。核验输出后才能声称自动恢复已生效。

明确退出或要求在当前对话执行时，先停用本对话再处理。普通“实现这个”“继续”“输出提示词”不退出；退出不要求固定口令。用户只要求退出时不开始项目任务。

## 状态和恢复

`C:\Users\xiao\.codex\state\voice-task-router\<session-id>.json` 只存所属 ID、模式标记、来源与更新时间，不存需求正文。脚本以安装目录定位状态文件，避免沙箱用户 HOME 或工作目录变化导致读取错误。事件使用自身 `session_id`，不是环境中的占位 ID。

已登记对话在 `UserPromptSubmit` 和 `SessionStart` 收到短的核心流程，包括“有关联工作对话就每轮重新读取上下文”、精简目标提示词、整体任务选型和按需协作。提醒本身不是读取证据：模型必须实际调用对话读取工具；同一轮已读可复用，上一轮和压缩前的读取不能替代当前轮。普通后续事件不改状态；未登记且未明确调用的对话不注入。不再需要用户重复点名。脚本出错只报告提醒，不阻断输入，也不执行项目操作。

摘要保存模式与最新需求/草稿。模式标记不能恢复丢失的草稿正文；缺失时按当前对话证据恢复或问最小缺口，不能编造。旧对话在之前没有登记时，需要在修复后明确调用一次；此后由 Hook 自动登记和恢复。

## 核验边界

三件事分别核验：①Hook 原生配置已加载且信任；②目标对话确有激活记录；③真实后续回合收到提醒并按契约交付。仅 `enabled/trusted` 不证明②或③，脚本单元测试也不证明模型永远遵守角色。

尤其是侧栏临时对话：关联的主项目链接不是侧栏自身 ID。没有本轮 Hook 或原生元数据给出实际 UUID 时，不能借主项目 ID 登记或宣称持久化已验证。可以继续本轮需求工作，并说明自动恢复是否可核验；不要用主对话测试代替侧栏实际回合测试。

原生 Hook 必须在用户当前 Codex 主机启用、信任。修改 Hook 定义需正常原生审阅；不编辑信任哈希或伪装托管政策。不扩大到其他客户端或主机。当前修复复用两项已有事件；无需添加自动执行或不断续跑的 Hook。

[官方 Skills](https://learn.chatgpt.com/docs/build-skills)说明加载方式；[官方 Hooks](https://learn.chatgpt.com/docs/hooks)说明 `prompt`、`session_id`、developer context 和原生信任机制。
