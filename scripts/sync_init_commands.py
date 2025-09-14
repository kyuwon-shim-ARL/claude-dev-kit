#!/usr/bin/env python3
"""
자동 커맨드 동기화 스크립트
.claude/commands/ 디렉토리의 실제 파일들과 init.sh의 commands 배열을 자동으로 동기화
"""

import os
import re
import sys
from pathlib import Path

def get_actual_commands():
    """실제 .claude/commands/ 디렉토리에서 커맨드 파일들을 스캔"""
    commands_dir = Path(__file__).parent.parent / ".claude" / "commands"

    if not commands_dir.exists():
        print(f"❌ Commands directory not found: {commands_dir}")
        return []

    commands = []
    for file in commands_dir.glob("*.md"):
        if file.name != "index.md" and not file.name.startswith("test_"):
            command_name = file.stem
            commands.append(command_name)

    return sorted(commands)

def update_init_script(commands):
    """init.sh의 commands 배열을 업데이트"""
    init_path = Path(__file__).parent.parent / "init.sh"

    if not init_path.exists():
        print(f"❌ init.sh not found: {init_path}")
        return False

    # 현재 init.sh 읽기
    with open(init_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # commands 배열 부분 찾기
    pattern = r'declare -A commands=\(\s*([^)]+)\s*\)'

    # 새로운 commands 배열 생성 (bash 문법: = 주위 공백 없음)
    command_entries = [f'        ["{cmd}"]="{cmd}"' for cmd in commands]
    new_commands = "declare -A commands=(\n" + "\n".join(command_entries) + "\n    )"

    # 교체
    new_content = re.sub(
        pattern,
        new_commands.replace('\n', '\n        '),
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # 파일 쓰기
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    print("🔄 커맨드 동기화 시작...")

    # 1. 실제 커맨드 파일들 스캔
    actual_commands = get_actual_commands()
    print(f"📁 발견된 커맨드: {len(actual_commands)}개")
    for cmd in actual_commands:
        print(f"  - {cmd}")

    if not actual_commands:
        print("❌ 커맨드 파일을 찾을 수 없습니다.")
        return 1

    # 2. init.sh 업데이트
    if update_init_script(actual_commands):
        print("✅ init.sh 업데이트 완료")
        print(f"📊 총 {len(actual_commands)}개 커맨드로 동기화됨")
    else:
        print("❌ init.sh 업데이트 실패")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())