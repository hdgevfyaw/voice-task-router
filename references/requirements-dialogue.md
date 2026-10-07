# Discuss requirements and choose the next step

Use this for the continuing side-chat discussion and progress-based next-step requests. Prompt translation lives in [voice-prompting.md](voice-prompting.md); model comparisons live in [model-routing.md](model-routing.md). Do not reprint this workflow to the user.

## Keep one evolving requirement

Track the current goal and target; settled constraints and priorities; assistant proposals still under discussion; material unknowns; the latest editable draft; and project facts with their source and freshness. This can remain in conversational context. Do not write a separate requirements file or reproduce the entire state on every turn.

Interpret a supplement against the current requirement. “还有一点” adds a compatible constraint; “这里改一下” changes the identified point; “不是这个意思” calls for repairing the interpretation. Restate a genuinely unclear correction before rewriting a misleading draft. A later correction does not erase unrelated earlier conditions. If the user clearly starts a different task, do not carry over old task-specific constraints.

Distinguish four things: what the user requested, what they explicitly accepted, what the assistant proposed, and what project evidence shows. Silence is not acceptance of a proposal, and a pasted or drafted prompt is not completion evidence. A sufficiently clear request can be drafted directly without being labelled “已确认”.

## Discuss only what blocks a faithful draft

A requirement is clear enough when the action, target, intended outcome, and material scope or stopping boundary are understood. Not every method or optional preference needs to be settled. The working AI can inspect ordinary implementation details.

When uncertainty would produce materially different tasks, briefly explain the understood goal and the one decision that changes the work most. Ask a focused question; use short choices if they reveal a useful distinction. Do not interrogate the user with a full requirements questionnaire. If the user is exploring an idea, help reason about goals, options, and tradeoffs instead of prematurely producing an execution prompt.

User uncertainty about the goal and uncertainty the work should investigate are different. “我还不知道要做成什么” may need discussion. “先查清问题原因，再决定如何修” can be a clear investigation task; draft it with the user's stopping boundary. Do not force certainty about facts the requested work is meant to discover.

Once the requirement is sufficiently clear, return the editable draft immediately. If it is partially unresolved but a provisional draft aids discussion, mark the open decision explicitly and do not invent its answer. When the user explicitly asks for the prompt, deliver a provisional draft and clearly conditional model/effort recommendation in that turn rather than only summarizing or asking another question. Avoid presenting a conditional recommendation as settled when the unresolved interpretation changes the model requirement.

## Revise the draft without restarting the conversation

When a draft exists, briefly state the correction and provide the complete updated prompt in one copyable block. A patch alone forces the user to merge prompts manually. For a small edit, keep the explanation short and do not repeat the project history, model evidence, or full routing analysis.

Reassess the model when the task expands, changes action, gains consequential uncertainty, adds interdependent subtasks, changes quality requirements, or changes the completion-efficiency constraint. Otherwise keep the existing recommendation and write its full model name and exact effort again alongside the revised prompt; “unchanged” alone is not a complete handoff. Apply the existing quality/efficiency/cost objective; do not choose a cheaper model by removing difficult requested work.

If the user only discusses or corrects the wording, remain in discussion. Do not treat “这样更好”“按这个改” about the draft as permission to implement the underlying work here. If they explicitly want a stage of discussion or review before editing, preserve it in the work prompt. If they requested a complete implementation, calling its prompt a draft does not insert a new approval gate in the destination task.

## “下一步” means a fresh progress-based recommendation

Read [active-project.md](active-project.md), then fetch the linked thread's latest status and relevant turns. If the user explicitly selects a different project, use that project. Rely on actual progress evidence, not a previously generated prompt or a cached summary. Do not reread unrelated history merely to provide a recommendation.

From the latest evidence, determine the current goal, completed work, active work, and the constraint preventing useful progress. Prefer a step that resolves a prerequisite or blocker, completes an unfinished requested outcome, or delivers the next useful result. Consider dependencies, benefit, risk of rework, and the effort needed; do not invent priority scores or assume that the most technically difficult task is the best next step.

Recommend **one** actionable step with a brief reason tied to the latest facts. If the project is awaiting a user decision, helping resolve that decision may be the appropriate next step. If work is still active, do not infer completion or recommend parallel duplication; propose a useful independent action only when grounded. Do not interrupt, dispatch work, or change chats automatically.

Use the chosen step's actual scope to select the model/effort, not the complexity of the whole project. Give its prompt with sufficient inputs, constraints, and stopping boundary. Retain a concise connection to the overall goal when needed. If the step has substantial delegable work, the host/worker arrangement belongs inside this same prompt under [hybrid-delegation.md](hybrid-delegation.md).

If progress is unreadable or decisive evidence is missing, say exactly what could not be established. Ask the smallest question that makes the next-step choice possible, such as whether the last proposed change was executed and what its result was. The user can provide current progress or a working link. A provisional draft is allowed when useful; an ungrounded claim that it is the best next step is not.

## Examples of the interaction

**Vague goal → discussion → draft.** User: “这个页面不太对，想让它更好用。” With no evidence identifying the problem, ask whether the goal is finding information more easily or reducing the steps to complete an action. User: “主要是找到导出入口，不要动导出逻辑。” Now draft a task to improve the discoverability of the existing export entry while preserving export behavior; do not keep asking about fonts, architecture, or optional polish.

**Correction preserves earlier constraints.** Draft requirement: improve a supplied SQL query's performance, preserve result semantics, and do not execute it. User: “再补一点，优先考虑可读性，不要为了小幅提速写得很复杂。” Update the prompt to preserve semantics and no-execution, prioritize readability, and avoid complexity for marginal performance gains. Do not discard the performance goal or add a database benchmark the user forbade. Reassess the model only if this changes the actual difficulty.

**Fresh progress changes the next step.** Latest project evidence says an implementation is complete but its required validation is pending. The next recommendation should target the pending validation, not repeat implementation. If instead the latest evidence shows implementation still running, do not assume it completed because the previous side-chat prompt described it. A verification prompt must carry existing constraints and checks supported by the work, not an invented release or deployment.

These illustrate decision rules, not mandatory task categories, output templates, or model mappings.
