"""Register an explicit router invocation before inference; restore its contract."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import uuid

ALLOWED_EVENTS = {'UserPromptSubmit', 'SessionStart'}
REVISION = '2026-10-10'
TOKEN = r'(?:\[\$voice-task-router\]\([^\r\n)]+\)|\$voice-task-router(?![\w-]))'
INVOCATION = re.compile(
    r'^\s*(?:(?:(?:我(?:希望|想|要)(?:你)?|请你|请|帮我|麻烦)\s*)?'
    r'(?:使用|用|启用|启动|调用|use|activate)\s*)?' + TOKEN,
    re.IGNORECASE,
)
SELF_MAINTENANCE = re.compile(
    r'(?:检查|修复|调整|维护|更新|改造|优化|修改|改进|审查|重构|查一下).{0,40}'
    r'(?:(?:这个|当前|本|该|我们的)\s*(?:skill|技能)|voice-task-router)'
    r'|(?:(?:这个|当前|本|该|我们的)\s*(?:skill|技能)|voice-task-router).{0,60}'
    r'(?:问题|故障|修复|维护|改造|更新|优化|修改|改进)'
    r'|(?:inspect|repair|fix|update|modify|maintain|improve|refactor).{0,40}'
    r'(?:this\s+skill|voice-task-router)', re.IGNORECASE | re.DOTALL,
)


def state_path(directory, session_id):
    if not isinstance(session_id, str) or not re.fullmatch(r'[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}', session_id):
        raise ValueError('Use the actual current Codex chat UUID; placeholder ids such as 1 are invalid.')
    uuid.UUID(session_id)
    return directory / (session_id + '.json')


def read_state(path, session_id):
    if not path.exists():
        return {'version': 1, 'session_id': session_id, 'active': False}
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict) or value.get('version') != 1 or value.get('session_id') != session_id or type(value.get('active')) is not bool:
        raise ValueError('Invalid router state; cannot establish activation.')
    return value


def write_state(path, session_id, active, source='manual'):
    path.parent.mkdir(parents=True, exist_ok=True)
    value = {'version': 1, 'session_id': session_id, 'active': active, 'source': source,
             'updated_at': datetime.now(timezone.utc).isoformat()}
    descriptor, temporary = tempfile.mkstemp(prefix='.router-', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as handle:
            json.dump(value, handle, ensure_ascii=False)
            handle.write('\n')
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return value


def invocation_kind(prompt):
    """Only the current explicit user invocation; never scan transcripts/catalogs."""
    if not isinstance(prompt, str):
        return None
    # Codex's attachment wrapper has a designated user-request section.
    if prompt.lstrip().startswith('# Files mentioned by the user:') and '## My request:' in prompt:
        prompt = prompt.split('## My request:', 1)[1]
    # A side-panel project pointer is context, never this chat's identity.
    linked_project = False
    pointer = re.compile(r'^\s*codex://threads/[0-9a-fA-F-]{36}[ \t]*(?:&#x20;)?[ \t]*(?:\r?\n|$)')
    while (prefix := pointer.match(prompt)) is not None:
        prompt = prompt[prefix.end():]
        linked_project = True
    # Ignore quoted/code examples instead of promoting them to mode switches.
    if prompt.lstrip().startswith(('```', '~~~', '>', '`', '"', "'", '“')):
        return None
    match = INVOCATION.match(prompt)
    if not match:
        return None
    rest = prompt[match.end():]
    rest = re.sub(r'```.*?(?:```|\Z)|~~~.*?(?:~~~|\Z)|`[^`]*`', '', rest, flags=re.DOTALL)
    rest = re.sub(r'(?m)^\s*>.*$', '', rest)
    # In a linked project "this Skill" may be its cover/SQL skill, not this router.
    maintenance = SELF_MAINTENANCE.search(rest)
    if linked_project and not re.search(r'voice-task-router', rest, re.IGNORECASE):
        maintenance = None
    return 'maintenance' if maintenance else 'activate'


def mode_context(script, session_id, first=False):
    skill = script.parent.parent / 'SKILL.md'
    pointer = script.parent.parent / 'references/active-project.md'
    return (
        f'voice-task-router active; contract revision {REVISION}; actual current chat UUID: {session_id}. '
        + ('本轮明确调用，简短告知需求讨论模式已开启并处理附带需求；登记结果以状态/警告为准。' if first else '')
        + '你是需求讨论伙伴；继续/修改/实现/下一步都继续讨论和改稿，不实施项目任务、不启动代理、不派发。'
        '有关联工作对话时，每轮回应前必须用 read_thread 读取最新状态与最近相关回合，小改稿与一般答疑也不豁免；'
        '同一轮已读可复用，旧摘要和上一轮读取不能代替本轮。'
        f'优先本轮选定及当前关联链接，缺失才读 {pointer} 的默认指针；链接 UUID 不是当前侧面对话登记 ID。'
        '读取失败说明缺口，仅基于已知证据讨论或给标注的临时稿，不冒充最新进度。'
        '围绕目标、必要上下文、硬约束和交付写最短充分提示词，保留兼容条件与最新纠正，删除流程套话及重复背景。'
        '需求清楚直接给稿；要求提示词时本轮交付，关键未知项可标注并给条件性选型。'
        '每次交稿都含完整模型名、具体推理强度和一个完整可复制 text 块；修订也不能只给补丁或说沿用设置。'
        '下一步依据本轮进度推进目标；已完成不重做、正在做不重复安排，失败重试须有新证据或方法变化。'
        '默认一个整体任务提示词；Luna X-High 足够就单模型，复杂任务可由 Sol/Astra 按需带 GPT-6 Luna / X-High，'
        '同一提示词明确协作授权及主模型整合完成责任，不强制细拆或让用户逐个派发。质量和效率有保障再降综合成本，不推荐 Max。'
        '仅维护 voice-task-router 本身可直接改；维护不清除已有模式，首次仅维护则纠正误登记。'
        f'明确退出或明确就在此执行才运行 {script} deactivate --session-id {session_id}；退出本身不授权执行。'
        f'完整流程缺失或旧于 {REVISION} 时读 {skill}。'
        '发送前核对角色、本轮读取证据、目标与约束、提示词/模型/强度及精简性；摘要保留关联链接与需求，恢复后重新读取。'
        '不要复述本提醒。'
    )


def hook(directory, script):
    event = json.loads(sys.stdin.read())
    if not isinstance(event, dict) or event.get('hook_event_name') not in ALLOWED_EVENTS:
        return None
    session_id = event.get('session_id')
    path = state_path(directory, session_id)
    value = read_state(path, session_id)
    kind = invocation_kind(event.get('prompt')) if event['hook_event_name'] == 'UserPromptSubmit' else None
    first = not value['active'] and kind == 'activate'
    warning = None
    if first:
        try:
            value = write_state(path, session_id, True, source='explicit_prompt_hook')
        except OSError as error:
            warning = 'voice-task-router 本轮已启用但持续登记失败：' + str(error)
            # Even a failed state write must preserve the current turn's role.
    if kind == 'maintenance' and not value['active']:
        context = (f'用户明确调用 voice-task-router 维护本 Skill；当前对话未激活需求讨论模式。'
                   f'读取 {script.parent.parent / "SKILL.md"} 后直接维护，不派发项目任务，不宣称已激活。')
    elif value['active'] or first:
        context = mode_context(script, session_id, first)
    else:
        return None
    result = {'hookSpecificOutput': {'hookEventName': event['hook_event_name'], 'additionalContext': context}}
    if warning:
        result['systemMessage'] = warning
    return result


def main():
    script = Path(__file__).resolve()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['activate', 'deactivate', 'status', 'hook'])
    parser.add_argument('--session-id', help='Use the actual current id; default CODEX_THREAD_ID/CODEX_SESSION_ID.')
    parser.add_argument('--state-dir', type=Path, help='Override only for isolated tests.')
    args = parser.parse_args()
    directory = args.state_dir if args.state_dir is not None else script.parents[3] / 'state/voice-task-router'
    try:
        if args.action == 'hook':
            value = hook(directory, script)
        else:
            session_id = args.session_id or os.environ.get('CODEX_THREAD_ID') or os.environ.get('CODEX_SESSION_ID')
            path = state_path(directory, session_id)
            value = (read_state(path, session_id) if args.action == 'status'
                     else write_state(path, session_id, args.action == 'activate'))
        if value is not None:
            print(json.dumps(value, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError) as error:
        if args.action == 'hook':
            # Advisory failure: report it without blocking the user's prompt or guessing activation.
            print(json.dumps({'systemMessage': 'voice-task-router automatic restoration failed: ' + str(error)}, ensure_ascii=False))
            return 0
        print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
