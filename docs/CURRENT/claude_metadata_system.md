# Claude 내장 메타데이터 시스템 설계

## 🎯 핵심 원칙
- **Zero Installation**: 추가 설치 없음
- **Claude Native**: Claude가 직접 처리
- **Invisible but Powerful**: 사용자는 몰라도 자동 작동

## 📋 메타데이터 형식

### HTML 주석 방식 (권장)
```markdown
<!--
@meta
id: doc_20250901_auth_guide
type: tutorial
parent: PRD_v3
status: draft
created: 2025-09-01
triggers: auth.py, auth_test.py
-->

# 실제 문서 내용
```

### 왜 HTML 주석?
- Markdown 렌더링에 영향 없음
- GitHub에서도 보이지 않음
- Claude가 쉽게 파싱 가능

## 🔄 자동 처리 흐름

### 문서 생성 시
```
1. Claude가 문서 생성 요청 받음
2. 문서 타입 자동 감지 (파일명, 내용 분석)
3. 현재 컨텍스트에서 parent 추출
4. 메타데이터 자동 삽입
5. 파일 저장
```

### 문서 수정 시
```
1. 기존 메타데이터 확인
2. updated 필드만 갱신
3. status 필요시 변경 (draft → review)
```

### 문서 정리 시 (/문서정리)
```
1. 모든 .md 파일 스캔
2. 메타데이터 파싱
3. 관계 그래프 메모리에 구축
4. 스마트 정리 제안
```

## 📊 메타데이터 필드

| 필드 | 설명 | 자동 생성 |
|------|------|----------|
| id | 고유 식별자 | ✅ |
| type | 문서 타입 (tutorial/planning/api/test) | ✅ |
| parent | 부모 문서 ID | ✅ |
| status | draft/review/published/archived | ✅ |
| created | 생성 일시 | ✅ |
| updated | 수정 일시 | ✅ |
| triggers | 관련 코드 파일 | ✅ |
| tags | 사용자 정의 태그 | ❌ |

## 🎨 문서 타입 자동 감지 규칙

```python
def detect_document_type(filename, content):
    # 파일명 기반
    if 'guide' in filename or 'tutorial' in filename:
        return 'tutorial'
    if 'PRD' in filename or 'plan' in filename:
        return 'planning'
    if 'test' in filename:
        return 'test'
    if 'api' in filename or 'reference' in filename:
        return 'api'
    
    # 내용 기반
    if '## Steps' in content or '## Prerequisites' in content:
        return 'tutorial'
    if '## Requirements' in content or '## Goals' in content:
        return 'planning'
    
    return 'documentation'
```

## 🔗 관계 추적 (메모리 내)

Claude는 세션 중에 문서 관계를 메모리에 유지:

```
PRD_v3
├── auth_guide.md (tutorial)
├── auth_test.md (test)
└── api_auth.md (api)

auth.py
├── triggers: auth_guide.md
└── triggers: auth_test.md
```

## 💡 사용 예시

### 예시 1: 문서 생성
```
User: "인증 가이드 문서 만들어줘"
Claude: [auth_guide.md 생성 with 메타데이터]
```

### 예시 2: 관계 확인
```
User: "현재 문서 구조 보여줘"
Claude: [메타데이터 분석 → 트리 구조 출력]
```

### 예시 3: 스마트 정리
```
User: "/문서정리"
Claude: 
- 30일 이상 draft: 3개 → archive 제안
- 고아 문서: 2개 → parent 연결 제안
- 중복 가이드: 2개 → 통합 제안
```

## ✅ 장점
1. **설치 불필요**: 바로 사용 가능
2. **투명성**: 메타데이터가 문서에 포함되어 있어 확인 가능
3. **이식성**: 다른 프로젝트로 복사해도 메타데이터 유지
4. **Git 친화적**: 텍스트 기반이라 diff 확인 용이
5. **점진적 적용**: 기존 문서도 수정 시 자동 추가