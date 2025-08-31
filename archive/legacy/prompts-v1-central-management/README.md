# Claude Dev Kit 프롬프트 관리 시스템

## 🎯 단일 진실 공급원 (Single Source of Truth)

모든 프롬프트는 `prompts/api.json`에서 중앙 관리되며, 다양한 클라이언트용 포맷이 자동 생성됩니다.

## 📁 구조

```
prompts/
├── api.json                    # 📡 중앙 프롬프트 저장소
├── sync-prompts.py            # 🔄 동기화 스크립트
├── claude-commands/           # Claude Code 슬래시 명령어
│   ├── 기획.md
│   ├── 구현.md  
│   ├── 안정화.md
│   └── 배포.md
├── raw/                       # 순수 텍스트 (외부 API용)
│   ├── 기획.txt
│   ├── 구현.txt
│   ├── 안정화.txt
│   └── 배포.txt
└── telegram-format/           # 텔레그램 봇용 JSON
    ├── 기획.json
    ├── 구현.json
    ├── 안정화.json
    ├── 배포.json
    ├── 전체사이클.json
    ├── 개발완료.json
    ├── 품질보증.json
    └── 실행완료.json
```

## 🔄 동기화 워크플로우

### 1. 프롬프트 수정
```bash
# api.json만 수정
vim prompts/api.json
```

### 2. 모든 포맷 재생성
```bash
# 한 번에 모든 포맷 동기화
python prompts/sync-prompts.py
```

### 3. 각 클라이언트에서 업데이트

**Claude Code:**
```bash
# 프로젝트별 설치
cp prompts/claude-commands/* .claude/commands/

# 전역 설치 (권장)
cp prompts/claude-commands/* ~/.claude/commands/
```

**claude-ops (텔레그램):**
```python
# GitHub에서 직접 fetch
import requests

def get_telegram_prompt(keyword):
    url = f"https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/prompts/telegram-format/{keyword}.json"
    return requests.get(url).json()

# 사용
prompt_data = get_telegram_prompt("안정화")
bot.send_message(chat_id, prompt_data["message"])
```

**외부 API 연동:**
```bash
# HTTP GET으로 직접 사용
curl https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/prompts/raw/안정화.txt
```

## 🎯 장점

### ✅ 단일 진실 공급원
- **api.json 하나만 수정** → 모든 클라이언트 자동 동기화
- 버전 관리 및 히스토리 추적

### ✅ 다중 클라이언트 지원
- **Claude Code**: 슬래시 명령어
- **텔레그램**: JSON 포맷 버튼
- **외부 도구**: Raw text API

### ✅ 자동화
- `sync-prompts.py` 한 번 실행으로 모든 포맷 생성
- Git hook 연동 가능

## 🚀 claude-ops 연동 예시

```python
# claude-ops에서 claude-dev-kit 프롬프트 활용
import requests
import json

class ClaudeDevKitPrompts:
    BASE_URL = "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/prompts"
    
    def get_prompt(self, keyword, format_type="telegram"):
        """Get prompt in specified format"""
        if format_type == "telegram":
            url = f"{self.BASE_URL}/telegram-format/{keyword}.json"
            return requests.get(url).json()
        elif format_type == "raw":
            url = f"{self.BASE_URL}/raw/{keyword}.txt"
            return requests.get(url).text
    
    def get_workflow_prompt(self, workflow="전체사이클"):
        """Get combined workflow prompt"""
        url = f"{self.BASE_URL}/telegram-format/{workflow}.json"
        return requests.get(url).json()

# 사용
prompts = ClaudeDevKitPrompts()
안정화_prompt = prompts.get_prompt("안정화")
send_to_claude(안정화_prompt["message"])
```

이제 **claude-ops는 프롬프트를 직접 관리할 필요 없이**, claude-dev-kit에서 최신 프롬프트를 자동으로 가져와 사용할 수 있습니다! 🎯