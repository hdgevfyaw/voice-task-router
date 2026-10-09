# Active project thread

Set this optional pointer to the Codex conversation that represents your active project. Keep the pointer user-specific; use the placeholder below in shared or public copies.

Current link:

`codex://threads/<your-active-project-thread-uuid>`

Treat this as the active project context until the user explicitly replaces it. Whenever a work chat is associated, fetch its latest state and recent relevant turns before every reply in the discussion chat, including questions, corrections, and prompt revisions. A read in the current turn can be reused; a previous-turn summary cannot replace a fresh read. Read only the recent context needed and fetch older turns when an important fact is missing.

Track the goal, completed and active work, blockers, and the last attempt and result. Do not repeat completed or active work. After a failed attempt, propose a retry only when new evidence or a changed approach can move the task forward. This file stores the pointer, not a substitute for reading current progress.

When the user explicitly says the active project link changed and supplies its replacement, update the pointer before reading the new thread. Do not replace it when a link is quoted as an example. If the link cannot be opened, report the gap and request a usable link or current context rather than claiming to know the latest progress.
