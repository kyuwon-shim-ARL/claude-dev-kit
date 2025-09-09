<!--
@meta
id: document_20250905_1110_claude-ops-integration
type: document
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-05
tags: claude-ops-integration.md, claude, development, integration, ops
related: 
-->

# Claude-Ops 텔레그램 통합 가이드

## 📱 텔레그램 버튼식 컨텍스트 관리

### 구조화된 명령어 템플릿 (JSON)

```json
{
  "context_management": {
    "commands": [
      {
        "id": "compact_deploy",
        "label": "🚀 배포 후 정리",
        "command_template": "/compact \"v{VERSION} 배포 완료. ZEDS 문서 보존됨. 구현 과정 제거\"",
        "params": ["VERSION"],
        "expected_reduction": "75-85%",
        "button_color": "primary"
      },
      {
        "id": "compact_planning",
        "label": "📋 기획 후 정리",
        "command_template": "/compact \"기획 완료. planning.md 저장됨. 탐색 과정 제거\"",
        "params": [],
        "expected_reduction": "70-80%",
        "button_color": "info"
      },
      {
        "id": "compact_implementation",
        "label": "⚡ 구현 후 정리",
        "command_template": "/compact \"구현 완료. 코드 변경 저장됨. 디버깅 과정 제거\"",
        "params": [],
        "expected_reduction": "70-80%",
        "button_color": "success"
      },
      {
        "id": "compact_stabilization",
        "label": "🔧 안정화 후 정리",
        "command_template": "/compact \"안정화 완료. test-report.md 저장됨. 오류 수정 과정 제거\"",
        "params": [],
        "expected_reduction": "75-85%",
        "button_color": "warning"
      },
      {
        "id": "compact_general",
        "label": "🧹 일반 정리",
        "command_template": "/compact \"작업 완료. ZEDS 문서 보존됨. 작업 과정 제거\"",
        "params": [],
        "expected_reduction": "60-70%",
        "button_color": "secondary"
      },
      {
        "id": "clear_all",
        "label": "🔄 전체 초기화",
        "command_template": "/clear",
        "params": [],
        "expected_reduction": "100%",
        "button_color": "danger",
        "confirmation_required": true
      }
    ],
    "quick_actions": [
      {
        "id": "check_context",
        "label": "📊 컨텍스트 상태",
        "command": "/memory",
        "button_color": "light"
      },
      {
        "id": "save_session",
        "label": "💾 세션 저장",
        "command": "/save",
        "button_color": "light"
      }
    ]
  }
}
```

### 텔레그램 봇 인터페이스 예시

```python
# claude_ops_telegram_bot.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json

class ContextManagementBot:
    def __init__(self):
        with open('context_commands.json', 'r') as f:
            self.config = json.load(f)
    
    def create_context_keyboard(self):
        """컨텍스트 관리 버튼 키보드 생성"""
        keyboard = []
        
        # 주요 정리 명령어 버튼들
        for cmd in self.config['context_management']['commands']:
            if cmd['id'] != 'clear_all':  # clear는 별도 행에
                button = InlineKeyboardButton(
                    text=cmd['label'],
                    callback_data=f"ctx_{cmd['id']}"
                )
                keyboard.append([button])
        
        # Clear 버튼은 별도 행에 (위험)
        clear_cmd = next(c for c in self.config['context_management']['commands'] 
                        if c['id'] == 'clear_all')
        keyboard.append([
            InlineKeyboardButton(
                text=f"⚠️ {clear_cmd['label']} ⚠️",
                callback_data="ctx_clear_all"
            )
        ])
        
        # 빠른 액션 버튼들
        quick_buttons = []
        for action in self.config['context_management']['quick_actions']:
            quick_buttons.append(
                InlineKeyboardButton(
                    text=action['label'],
                    callback_data=f"quick_{action['id']}"
                )
            )
        keyboard.append(quick_buttons)
        
        return InlineKeyboardMarkup(keyboard)
    
    def handle_callback(self, callback_query):
        """버튼 클릭 처리"""
        data = callback_query.data
        
        if data.startswith('ctx_'):
            cmd_id = data.replace('ctx_', '')
            command = self.get_command(cmd_id)
            
            if command.get('confirmation_required'):
                # 위험한 명령어는 확인 요청
                return self.request_confirmation(command)
            
            if command.get('params'):
                # 파라미터가 필요한 경우
                return self.request_params(command)
            
            # 즉시 실행
            return self.execute_command(command)
        
        elif data.startswith('quick_'):
            action_id = data.replace('quick_', '')
            return self.execute_quick_action(action_id)
    
    def execute_command(self, command):
        """명령어 실행"""
        cmd_text = command['command_template']
        
        # 파라미터 치환 (있는 경우)
        if hasattr(self, 'current_params'):
            for param, value in self.current_params.items():
                cmd_text = cmd_text.replace(f"{{{param}}}", value)
        
        return {
            'execute': cmd_text,
            'message': f"✅ 실행중: {command['label']}\n"
                      f"예상 감소율: {command['expected_reduction']}\n"
                      f"명령어: {cmd_text}"
        }
    
    def create_status_message(self, context_usage):
        """상태 메시지 생성"""
        if context_usage > 80:
            status = "🔴 정리 필요!"
            recommendation = "배포 후 정리 권장"
        elif context_usage > 60:
            status = "🟡 주의"
            recommendation = "곧 정리 필요"
        else:
            status = "🟢 양호"
            recommendation = "작업 계속 가능"
        
        return f"""
📊 **컨텍스트 상태**
사용률: {context_usage}% {status}
권장사항: {recommendation}

아래 버튼으로 컨텍스트를 관리하세요:
        """
```

### 워크플로우 통합

```yaml
# claude-ops-workflow.yaml
name: Context Management Workflow

triggers:
  - on_deploy_complete:
      show_buttons:
        - compact_deploy
        - check_context
  
  - on_planning_complete:
      show_buttons:
        - compact_planning
        - save_session
  
  - on_high_context_usage:
      threshold: 70
      show_buttons:
        - compact_general
        - check_context
  
  - on_session_end:
      show_buttons:
        - save_session
        - compact_general
        - clear_all

automations:
  - auto_suggest:
      when: context_usage > 80
      message: "컨텍스트가 80%를 초과했습니다. 정리를 권장합니다."
      buttons:
        - compact_general
  
  - post_compact_check:
      after: compact_*
      action: check_context
      success_message: "✅ 컨텍스트가 {before}%에서 {after}%로 감소했습니다!"
```

### 사용자 경험 (UX)

```
텔레그램 채팅창:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Claude: 배포가 완료되었습니다! (v7.2.0)

📊 **컨텍스트 상태**
사용률: 91% 🔴 정리 필요!
권장사항: 배포 후 정리 권장

┌─────────────────────────┐
│ 🚀 배포 후 정리         │
├─────────────────────────┤
│ 📋 기획 후 정리         │
├─────────────────────────┤
│ ⚡ 구현 후 정리         │
├─────────────────────────┤
│ 🔧 안정화 후 정리       │
├─────────────────────────┤
│ 🧹 일반 정리            │
├─────────────────────────┤
│ ⚠️ 🔄 전체 초기화 ⚠️    │
├─────────────────────────┤
│ 📊 상태 | 💾 저장       │
└─────────────────────────┘

[사용자가 "🚀 배포 후 정리" 클릭]

Claude: ✅ 실행중: 배포 후 정리
예상 감소율: 75-85%
명령어: /compact "v7.2.0 배포 완료. ZEDS 문서 보존됨. 구현 과정 제거"

...

Claude: ✅ 컨텍스트가 91%에서 22%로 감소했습니다!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### API 엔드포인트 (claude-ops 서버)

```python
# claude_ops_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CompactRequest(BaseModel):
    command_id: str
    params: dict = {}
    user_id: str

@app.post("/api/context/compact")
async def execute_compact(request: CompactRequest):
    """컨텍스트 정리 실행"""
    
    # 명령어 템플릿 가져오기
    command = get_command_template(request.command_id)
    
    # 파라미터 치환
    cmd_text = substitute_params(command, request.params)
    
    # Claude Code에 명령 전송
    result = await claude_code_execute(cmd_text)
    
    # 결과 분석
    before_usage = result.get('before_context', 0)
    after_usage = result.get('after_context', 0)
    reduction = before_usage - after_usage
    
    return {
        "success": True,
        "command": cmd_text,
        "before": before_usage,
        "after": after_usage,
        "reduction": reduction,
        "message": f"컨텍스트가 {reduction}% 감소했습니다"
    }

@app.get("/api/context/status")
async def get_context_status():
    """현재 컨텍스트 상태 조회"""
    status = await claude_code_memory_status()
    
    return {
        "usage_percent": status.get('usage', 0),
        "tokens_used": status.get('tokens_used', 0),
        "tokens_limit": status.get('tokens_limit', 200000),
        "recommendation": get_recommendation(status.get('usage', 0))
    }

@app.post("/api/context/batch")
async def batch_operations(operations: list):
    """여러 작업 일괄 실행"""
    results = []
    
    for op in operations:
        if op['type'] == 'compact':
            result = await execute_compact(op)
        elif op['type'] == 'save':
            result = await save_session(op)
        results.append(result)
    
    return {"results": results}
```

## 🚀 통합 효과

1. **원클릭 실행**: 텔레그램 버튼 터치만으로 컨텍스트 관리
2. **시각적 피드백**: 사용률, 권장사항 즉시 확인
3. **자동화 가능**: 워크플로우 트리거로 자동 제안
4. **일괄 처리**: 여러 작업을 순차적으로 실행
5. **안전장치**: 위험한 명령어는 확인 단계 추가

## 📋 구현 체크리스트

- [x] 구조화된 명령어 템플릿 (JSON)
- [x] 텔레그램 봇 인터페이스 설계
- [x] 워크플로우 통합 명세
- [x] API 엔드포인트 정의
- [ ] 실제 claude-ops 저장소에 PR
- [ ] 테스트 및 검증

---
*이 통합으로 컨텍스트 관리가 모바일에서도 버튼 하나로 가능해집니다*