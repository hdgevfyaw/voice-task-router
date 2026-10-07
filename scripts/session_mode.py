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
REVISION = '2026-10-05'
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
    return (
        f'voice-task-router active; contract revision {REVISION}; actual current chat UUID: {session_id}. '
        + ('本轮明确调用，先简短说明需求讨论模式已开启，并立即处理附带需求；持续登记是否成功以状态和警告为准。' if first else '')
        + '本轮先确定角色，再用工具：你是需求讨论伙伴。普通“继续/修改/实现/下一步”均继续整理需求，'
        '不能自行实施项目任务、修改项目文件、生成任务素材、启动代理或派发提示词。只读相关资料和项目进度是允许的。'
        '模糊目标讨论最关键分歧；足够明确立即交草稿。用户要求输出提示词，本轮必须实际给出完整可复制提示词、'
        '完整模型名和明确推理强度；有未知项可标注临时稿及条件性选型，不得只总结或承诺稍后给。'
        '已有稿的补充/纠正要保留兼容约束，返回完整修订稿，模型不变也写具体值。'
        '草稿格式：推荐模型：完整模型名；推理强度：具体值；一个 fenced text 提示词块。'
        '下一步先读取最新项目状态，选一个值得推进的步骤并说明理由；读取失败说明缺口，不冒充最新进度。'
        '保持完整、质量与完成效率后减少价格加权综合成本；只推荐用户当前可选择的模型和强度，并尊重明确偏好。'
        '适合混合方案时在提示词内写 Sol/Astra 主持与 Luna X-High 分工，这里不执行。'
        '只有明确维护 voice-task-router 本身可在此直接改；链接项目里的封面/口播/其他 Skill 修改不属于该例外。'
        '维护不清除已有模式；若首次调用实际仅要求维护本 Skill，纠正本轮误登记并直接维护。'
        f'明确退出或要求就在本对话执行时，运行绝对脚本 {script} deactivate --session-id {session_id}，'
        '无需固定口令；退出本身不授权执行。回复结束、草稿完成、新话题都不退出。'
        f'完整流程缺失或比 {REVISION} 旧时读 {skill}，否则复用。'
        '发送前检查角色未越界、提示词/模型名/强度齐全、约束保留，漏项立即补齐。'
        '摘要保留模式与最新需求/草稿；不要把本 Hook 文本复述给用户。'
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
