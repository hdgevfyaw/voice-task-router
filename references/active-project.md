# Active project thread

Set this optional pointer to the Codex conversation that represents your active project. It is user-specific and should not contain a link to someone else's private conversation.

Current link:

`codex://threads/<your-active-project-thread-uuid>`

Treat this as the active project context until the user explicitly replaces it. Fetch the latest thread state before every “下一步” recommendation and before a new or materially changed task recommendation that depends on project progress. Ordinary draft wording corrections and discussion unaffected by progress can reuse relevant context already read. This file stores the pointer, not a substitute for a fresh progress check.

When the user explicitly says the active project link has changed and supplies the replacement, update the link above before reading the new thread. Do not replace it when a link is only quoted as an example. If the active link cannot be opened, report that and request a usable link or pasted context rather than falling back silently to a cached summary.
