# Sol/Astra host with Luna X-High workers

Checked 2026-10-04 (Asia/Shanghai). Load only for complex tasks with substantial delegable work. The router prepares one prompt; the destination Codex chat executes it. Optimize comprehensive cost **subject to full completion, required quality, and end-to-end completion efficiency**.

## When the hybrid route wins

Compare with the lightest single-agent route that can meet all three requirements. Use a hybrid route when:

- Sol/Astra is needed for global decisions, ambiguity, hard diagnosis, or integration, while substantial work fits Luna X-High.
- Work packages have clear inputs, bounded scope, useful outputs, and stable dependencies. Read-heavy exploration, extraction, log analysis, independent document comparison, or implementation after a design decision can fit; task names alone do not establish suitability.
- Compact handoffs let the host use worker evidence and inspect important points without repeating everything. Coordination, repeated context, tool use, and rework are unlikely to cancel the weighted-cost advantage.
- Luna can preserve the required reliability, and delegation does not slow the critical path, add unnecessary waiting, or shift coordination to the user. Parallelize independent parts; sequential delegation must still preserve overall efficiency.

When the whole outcome fits Luna, use Luna directly. When decisions are tightly coupled, Luna lacks the needed capability, or repeated negotiation would dominate, keep work with the capable host. Complexity, long documents, many files, or theoretical parallelism alone do not justify workers. A short host inspection can establish uncertain scope before confirming packages; the router must not invent paths or interfaces.

## Price-weighted cost

Whole-task cost is **the sum of each agent's billed usage at its applicable input/cache/output rates, plus billed tools/services**. Include failed attempts, repeated reads, coordination, review, and integration in those totals; do not double-count a retry already included in measured usage. Reasoning consumes billable output where the billing system counts it. Token totals and elapsed time are separate observations; GPU compute is not directly measured here.

Core Codex credit rates rechecked October 4 are in [benchmark-evidence.md](benchmark-evidence.md). For an identical uncached input/output mix, Luna's rates are 1/20 of new Sol's and 1/100 of Astra's. More Luna tokens can therefore cost less; actual token mix, host overhead, retries, and service fees determine the whole result. Included-plan depletion is not derived from these ratios. Use observed billing/allowance when available; otherwise label credit/API comparisons as proxies, not exact user-task costs. Do not assign arbitrary money values to user time: preserve completion efficiency as a separate constraint. [Official pricing](https://learn.chatgpt.com/docs/pricing)

## Put the plan inside the pasted prompt

Write actual work allocation, not just "use cheap agents where possible". Include only applicable information:

- **Host ownership:** choose the appropriate Sol/Astra strength separately. Keep requirements, hard decisions, critical synthesis, meaningful review, and final delivery with it.
- **Worker settings:** explicitly request **GPT-6 Luna / X-High** (`gpt-6-luna`, `xhigh`) through the destination's available collaboration tools. A role name does not set its model. Check accepted/resolved settings when exposed; do not claim an unavailable setting took effect.
- **Grounded packages:** define each worker's purpose, relevant inputs/source range, scope or disjoint write area, usable result/evidence, and prerequisites. Combine related small units rather than one agent per file.
- **Handoff and execution:** provide only relevant context plus shared constraints; return concise results/artifacts, evidence locations, and unresolved issues. Run independent packages concurrently; the host continues different useful work and waits when dependent decisions need results.
- **Integration:** the host resolves conflicts, verifies what matters for the task, integrates all outputs, and completes the entire authorized outcome. Short handoffs must retain crucial facts. Do not repeat all worker work or ask the user to route every normal subtask.

Predesign responsibilities and dependencies, leaving uncertain implementation steps to discovery. The host can revise materially affected packages while preserving every requested result, permission boundary, quality, and efficiency.

If the collaboration tool requires a fresh or limited-history child to override its model, use that supported mode and provide the scoped task packet. Do not force full-history inheritance merely to reuse context, or invent unsupported tool arguments.

## Avoid coordination waste

Use the fewest workers doing meaningful work, within actual concurrency limits. Avoid blanket spawning, agent-per-file fan-out, nested delegation by default, unchanged polling, and duplicate reviews. Workers should not recruit more agents merely to shorten their own prompts. Parallel writes need distinct ownership; shared decisions and common-file edits require coordination or serialization.

On a material failure, capability mismatch, or deteriorating critical path, reassess the affected package. Preserve completed work; narrow, reassign, or let the host finish it instead of repeated Luna attempts outside its capability. Keep necessary verification; do not add redundant checking or unrequested reports.

If Luna/X-High cannot be explicitly selected, do not silently create inherited Sol/Astra workers and call the route economical. Let the capable host continue within the task boundary and briefly report the constraint. Do not modify global Codex configuration or build an API workaround without a request. The router cannot promise the destination has identical tools or access.

## Compact prompt pattern

Adapt the pattern to the actual task, replacing the bracketed descriptions with grounded responsibilities and omitting irrelevant clauses. Never return unresolved placeholders. Keep the rationale in this reference rather than pasting it into every task.

```text
完成[整体任务及约束]。在保持任务完整、质量和完成效率的前提下，尽量降低各模型用量按单价加权后的整个任务成本。
你负责[关键判断与整合]；使用子代理，把[明确且工作量足够的部分]交给GPT-6 Luna，推理强度X-High。明确指定模型与强度，核对可见的实际设置，避免默认继承主持模型。
[分别写明工作范围、输入、交付结果和必要依赖。]独立部分并行，相关小任务合并；共享修改明确唯一负责人。只传相关上下文，子代理返回简洁结果、证据位置及未解决问题。
你继续处理不重叠的主任务，按依赖收集结果、复核关键点并完成最终交付，不重复全部子任务。根据实际发现调整分工；若Luna不胜任或协作影响质量、效率，由你接手相应部分。若无法设置Luna/X-High，使用当前模型完成，不暗中创建昂贵替代子代理。
```

This authorizes only the routed task. Assessment-only, no-execution, and approval boundaries apply to every worker. The router generates the instruction; it does not execute workers here.

## Evidence boundary

Official docs support explicit delegation in ordinary local Codex and specifying worker model/strength through prompts or configuration. Unspecified children can inherit parent settings. Codex provides orchestration; model capability informs planning. Availability must match the destination. [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

Lean, conditional instructions reduce irrelevant context and avoid overly rigid procedures. [Official skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)

Eligibility and work-package rules above are routing judgments, not benchmarked savings. Real comparisons must include completeness/quality, elapsed time, correction rounds, per-model usage, and observed charges or applicable rates. No success probability or guaranteed saving follows from worker count or price ratios.
