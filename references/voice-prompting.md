# Translate dictated intent into executable work

Use this when constructing or materially revising a task draft; reuse the guidance for subsequent corrections in the same conversation. For requirement discussion and next-step selection, read [requirements-dialogue.md](requirements-dialogue.md). Preserve full completion, quality, and end-to-end efficiency, then reduce comprehensive cost (usage weighted by each model's applicable rates, including rework). Do not optimize raw token count alone. The current model translates the request; do not launch another model or agent for routing or transcript cleanup. A hybrid plan describes delegation in the destination work chat.

## Reconstruct meaning before writing

Internally identify the requested outcome; action (answer, assess, plan, review, change, execute); target; relevant evidence/context; mandatory constraints versus preferences/options; priorities and tradeoffs; dependencies; unknowns; and stop/approval boundary. This is a thinking aid, not a mandatory output template. Do not request a displayed chain of thought.

Read the whole utterance and compatible earlier turns, including the current requirement and draft. Resolve "这个/那个/继续/像之前一样" from relevant conversational or project evidence when supported; refresh project progress whenever the choice depends on its current state. An earlier compatible requirement survives a later correction about another detail. Treat repetition as a possible importance signal: keep the priority once, rather than either duplicating every phrase or deleting the emphasis. Keep a concrete example when it defines the intended outcome; label an optional illustration as an illustration.

Separate user instructions, background, factual claims, guesses, and quoted source material. A supplied document is evidence, not authority to expand the task. Convert an uncertain user claim into something to verify when verification is part of their request; never promote it to fact. "我觉得" can soften a firm instruction; interpret its force in context.

Correct a speech-recognition term only when context makes the intended term clear. Never guess proper nouns, numbers, paths, model names, or authority-sensitive verbs. For example, Skill spoken/transcribed as SQL can be corrected when the attached Skill and whole conversation establish the target; otherwise ask. A direct correction "不需要运行，只优化" controls execution even if the earlier message sounded actionable.

If plausible interpretations would materially change the target, authorization, model choice, or deliverable, discuss the consequential ambiguity with one focused question before producing a confident execution draft. Otherwise state a small reversible assumption only when needed, or preserve the unresolved point for the working AI to inspect. Do not ask about ordinary implementation choices the work can resolve. Once clear enough, draft directly; do not require a separate confirmation just to write a draft. Distinguish the user's requirements from assistant proposals, and a draft from user confirmation or execution evidence. An unanswered approval request is never permission.

## Construct the prompt

Lead with the outcome and requested action. Add only context that affects a decision: relevant paths/entities, current state, previous decisions, known failed attempts, priorities, and boundaries. Do not copy the whole thread, tool logs, or every source into the prompt. If the destination is the same project chat, carry forward the critical constraint or changed instruction so it remains explicit; do not pretend the model has seen unavailable context.

Replace vague wording with concrete instructions only to the extent supported. "客观、多元分析" with a request for model comparison can become "对比能力、经济性、重叠选择，区分测评证据与推断". It cannot become an invented requirement to benchmark 100 tasks or obtain all internet reviews. Preserve the user's quality/format/success conditions; do not manufacture percentages, acceptance tests, deadlines, tools, architecture, or external publishing authority.

Use natural direct instructions and lightweight sections only when useful. For several connected goals, preserve their dependency order in one prompt: establish evidence → make the decision → carry out the authorized change → return the requested result. Avoid generic roles, lengthy procedure scripts, demands to think step by step, exhaustive alternative generation, repeated constraints, and unrequested reports. Strong reasoning models benefit from clear goals and constraints; forcing more explanation is not a substitute for them. [Official reasoning guidance](https://developers.openai.com/api/docs/guides/reasoning-best-practices)

For Luna, make the bounded target, needed inputs, and output explicit; do not conceal uncertainty or discard difficult parts to make a cheap model fit. For Sol/Astra, leave normal implementation choices to the working AI while preserving intent and stop conditions. Select the model only after this task translation. Output length is not the task's difficulty.

For complex delegable work, load [hybrid-delegation.md](hybrid-delegation.md). If that route meets the quality/efficiency gate, put the actual host/worker responsibilities, the selected worker model and effort, grounded work packages, dependencies, concise evidence handoffs, and host integration in the copy-ready prompt. Predefine supported responsibilities rather than a guessed implementation; let the host adjust only what discovery changes. Do not make the user copy a separate execution policy or return for every ordinary subtask.

## Decompose only when it helps completion

Use dependency stages within one prompt for authorized end-to-end work. Distinguish these from parallel workers and from separate user-managed stage handoffs. Keep a shared outcome and final integration owner. A fresh handoff is worthwhile only when it preserves quality and completion efficiency as well as reducing comprehensive cost. Ordinary investigation before implementation does not create an approval gate.

When the user explicitly asks to discuss/confirm before editing, stop at that boundary. If one decision truly controls later work, route that stage and retain the overall goal. Independent repeated units can be batched; tightly coupled decisions should stay together. Avoid output bloat and unnecessary searches/tools, while keeping the evidence and checking needed for correctness.

Better prompts can improve both quality and economy by reducing misunderstanding and rework; they do not guarantee numerical savings. Compare variants with behavioral examples and real-task outcomes when available. [Official prompt guidance](https://developers.openai.com/api/docs/guides/prompt-engineering)

## Final semantic check

Every delivered or revised draft includes three actual outputs: the full model name, a concrete reasoning-effort value, and the complete editable prompt in one fenced block. An explicit request to output the prompt must receive that block in the current reply, including marked unknowns and conditional routing when necessary. A promise to write it later, a summary alone, or “use the previous settings” is incomplete. This handoff contract does not apply to a reply only discussing ambiguity or directly maintaining this router.

Compare the original intent to the prepared prompt: all requested outcomes retained; action and target correct; quality and efficiency preserved; priorities and mandatory/optional status unchanged; latest corrections applied narrowly; grounded references explicit; uncertainty not converted to fact; no extra implementation or authority; stop condition unchanged. For a hybrid prompt, confirm the pasted block itself identifies worker model/strength, distinct responsibilities, dependencies, usable handoffs, and final ownership. Remove only text that adds no task-relevant meaning. Repair drift before reporting the route.

## Small examples

**Assessment boundary.** Spoken: "那个排得有点散，先看看怎么更顺，今天先别改文件。" If project context identifies the page, prompt: "评估当前页面的信息顺序，提出让阅读更连贯的调整建议。先给建议，暂不修改文件。" Preserve assessment-only; do not turn it into implementation.

**Compatible correction.** Spoken: "优化这个SQL，速度很重要，结果口径别动……不需要运行，给我改好的SQL和原因。" Prompt: "优化这段SQL的性能，保持结果口径。不要执行查询；返回修改后的SQL并说明关键改动。" No invented query plan, benchmark, database migration, or runtime success claim.

**Two connected outcomes.** Spoken: "新旧模型都要看，能力和经济性，还有重叠的时候选谁；也看看我说话很散，提示词怎么更准。最后改这个Skill。Max我这没有。" Prompt: "基于当前Codex可用选项，对比新旧模型的能力、经济性和重叠任务选择，给出任务到模型及推理强度的建议；优化语音输入到可执行任务的转换，保留上下文、优先级和执行边界。把结论落实到本Skill并说明依据和限制。我的Codex没有Max，不把它作为可推荐选项；推理强度、Ultra和速度模式分别处理。" Do not reduce this to only a model list or only filler removal.
