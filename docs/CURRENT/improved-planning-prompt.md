<!--
@meta
id: document_20250905_1110_improved-planning-prompt
type: document
scope: operational
status: active
created: 2025-09-05
updated: 2025-09-09
tags: CURRENT, improved, planning, improved-planning-prompt.md, prompt
related: 
-->

# 개선된 기획 프롬프트 v2.0

## 🚨 핵심 수정사항

### 문제점 (기존)
```python
# 조건부 실행으로 거의 작동하지 않음
if (not exists('docs/specs/requirements.md') or 
    not exists('docs/specs/architecture.md') or
    prd_newer_than_specs() or
    detect_major_changes()):
```

### 해결책 (수정안)
```python
# PRD 생성시 항상 specs 분해 실행
def auto_generate_specs():
    if PRD_created_or_updated():
        # 필수 실행 (조건부 아님)
        extract_requirements(PRD) → docs/specs/requirements.md
        extract_architecture(PRD) → docs/specs/architecture.md
        maintain_project_rules() → docs/specs/project_rules.md
        
        # 세션별 진행상황만 CURRENT로
        session_planning → docs/CURRENT/session-planning.md
        active_todos → docs/CURRENT/active-todos.md
```

## 📋 수정된 프롬프트 섹션

**변경 전:**
```
📋 PRD 기반 사양서 자동 생성 (조건부 실행):
```

**변경 후:**
```
📋 PRD 기반 사양서 자동 생성 (필수 실행):

**자동 생성 트리거 (필수):**
- PRD 생성 또는 업데이트시 항상 실행
- 전략적 기획 (Strategic)에서만 실행

**생성 대상:**
- **requirements.md**: 모든 PRD에서 기능/비기능 요구사항 추출
- **architecture.md**: 시스템 구조, 컴포넌트, 데이터 흐름
- **project_rules.md**: 루트에서 specs로 이동 (최초 1회)

**docs/CURRENT 사용 원칙:**
- 세션별 임시 계획: session-planning.md  
- 진행 상황 추적: active-todos.md
- 테스트 결과: test-report.md
- 완성도 리포트: completion-report.md
- ❌ 영구적 아키텍처/요구사항 문서 금지
```

## 🔄 완전 수정된 프롬프트

### 📚 컨텍스트 자동 로딩 (수정됨)
**우선순위 순:**
- **docs/specs/project_rules.md** 확인 (프로젝트 헌법)
- **docs/specs/requirements.md** 확인 (요구사항)  
- **docs/specs/architecture.md** 확인 (아키텍처)
- **docs/specs/PRD-v*.md** 확인 (최신 PRD)
- **docs/CURRENT/session-planning.md** 확인 (세션 계획)
- **docs/CURRENT/active-todos.md** 확인 (진행 상황)

### 💾 규모별 차별화된 문서화 (수정됨)

**📋 PRD 기반 사양서 자동 생성 (필수 실행):**

**트리거 조건 (단순화):**
- 전략적 기획 (Strategic) 시 PRD 생성/업데이트
- 조건부 로직 제거, 항상 실행

**생성 프로세스:**
```python
def auto_generate_specs_v2():
    # PRD 생성시 필수 실행
    if strategic_planning_with_PRD():
        
        # 1. 불변적 내용 → docs/specs/
        extract_all_requirements() → docs/specs/requirements.md
        extract_all_architecture() → docs/specs/architecture.md
        ensure_project_rules() → docs/specs/project_rules.md
        
        # 2. 세션별 진행사항 → docs/CURRENT/
        create_session_plan() → docs/CURRENT/session-planning.md
        initialize_todos() → docs/CURRENT/active-todos.md
        
        # 3. 기존 CURRENT 내용 정리
        archive_completed_sessions() → docs/development/sessions/
```

**문서화 계층 (명확화):**

- **전략적 기획**: 
  - PRD 생성/업데이트 (docs/specs/)
  - **필수** specs 분해 (requirements.md, architecture.md)
  - 세션 계획 (docs/CURRENT/session-planning.md) 
  - TodoWrite (docs/CURRENT/active-todos.md)
  
- **전술적 기획**: 
  - 세션 계획 선택적 생성 (docs/CURRENT/)
  - TodoWrite (docs/CURRENT/active-todos.md)
  
- **운영적 작업**: 
  - TodoWrite만 (docs/CURRENT/active-todos.md)

## ✅ 기대 효과

1. **명확한 분리**: 불변 specs vs 가변 CURRENT
2. **자동 실행**: PRD 생성시 specs 분해 보장  
3. **정리된 구조**: CURRENT에 영구 문서 축적 방지
4. **일관된 참조**: specs를 참조점으로 활용