# 분석 기반 문서화 체계 v1.0

## 📊 문서 분류 체계

### 1. 분석 유형별 디렉토리 구조
```
docs/
├── CURRENT/           # 🔥 활성 작업 (ZEDS 통합)
├── analysis/          # 📊 분석 보고서
│   ├── performance/   # 성능 분석
│   ├── architecture/  # 구조 분석
│   ├── security/      # 보안 분석
│   ├── usability/     # 사용성 분석
│   ├── business/      # 비즈니스 분석
│   └── research/      # 🧬 연구 분석 (바이오인포매틱스)
│       ├── transcriptome/  # 전사체 분석
│       ├── genomics/       # 유전체 분석
│       ├── proteomics/     # 단백체 분석
│       └── integrated/     # 통합 오믹스
├── reports/           # 📄 정형 보고서
│   ├── weekly/        # 주간 보고
│   ├── monthly/       # 월간 보고
│   └── release/       # 릴리즈 보고
└── decisions/         # 🎯 의사결정 기록
    ├── technical/     # 기술 결정
    └── strategic/     # 전략 결정
```

## 🎯 분석 목적별 프롬프트 가이드

### 1. 성능 분석 (/분석 performance)
```markdown
"성능 병목 지점과 최적화 기회를 MECE 분석하여 
docs/analysis/performance/YYYYMMDD-{주제}.md로 저장해줘"
```
**산출물**: 벤치마크 결과, 병목 분석, 최적화 제안

### 2. 구조 분석 (/분석 architecture)
```markdown
"현재 시스템 아키텍처의 강점/약점/기회/위협을 분석하여
docs/analysis/architecture/YYYYMMDD-{주제}.md로 저장해줘"
```
**산출물**: 의존성 그래프, 모듈 결합도, 리팩토링 계획

### 3. 보안 분석 (/분석 security)
```markdown
"OWASP Top 10 기준으로 보안 취약점을 스캔하여
docs/analysis/security/YYYYMMDD-{주제}.md로 저장해줘"
```
**산출물**: 취약점 목록, 위험도 평가, 대응 방안

### 4. 사용성 분석 (/분석 usability)
```markdown
"사용자 워크플로우와 페인 포인트를 분석하여
docs/analysis/usability/YYYYMMDD-{주제}.md로 저장해줘"
```
**산출물**: 사용자 여정 지도, 개선 우선순위

### 5. 비즈니스 분석 (/분석 business)
```markdown
"ROI와 비용-효과를 정량적으로 분석하여
docs/analysis/business/YYYYMMDD-{주제}.md로 저장해줘"
```
**산출물**: 비용 분석, ROI 계산, 의사결정 지원

## 📝 문서 템플릿

### 표준 분석 문서 구조
```markdown
# [분석 제목]
날짜: YYYY-MM-DD
유형: [performance|architecture|security|usability|business]
작성자: Claude + [사용자]

## 요약 (Executive Summary)
- 핵심 발견사항 3-5개
- 주요 권고사항
- 예상 임팩트

## 분석 방법론
- 사용한 도구/프레임워크
- 데이터 수집 방법
- 분석 범위와 제약사항

## 상세 분석
### 1. 현황 (As-Is)
### 2. 문제점 (Problems)
### 3. 기회 (Opportunities)
### 4. 제안 (To-Be)

## 실행 계획
| 우선순위 | 작업 | 예상 공수 | 담당 |
|---------|------|----------|------|
| P0 | ... | ... | ... |

## 부록
- 원시 데이터
- 참고 자료
```

## 🔄 생명주기 관리

### 1. 생성 단계
- 분석 요청 시 자동으로 적절한 디렉토리에 생성
- 날짜-주제 네이밍으로 버전 관리

### 2. 활용 단계
- CURRENT/에 심볼릭 링크로 활성 분석 연결
- 의사결정 시 decisions/로 핵심 내용 추출

### 3. 보관 단계
- 3개월 이상 된 분석은 archives/로 이동
- 연간 종합 보고서에 주요 인사이트 통합

## 🚀 실행 가이드

### Quick Start
```bash
# 1. 분석 요청
/분석 performance "API 응답 시간 분석"

# 2. Claude가 자동으로:
- 적절한 도구로 데이터 수집
- MECE 프레임워크로 분석
- docs/analysis/performance/에 보고서 생성

# 3. 후속 조치
/전체사이클 "분석 결과 기반 최적화 구현"
```

### 통합 워크플로우
```mermaid
graph LR
    A[분석 요청] --> B[데이터 수집]
    B --> C[MECE 분석]
    C --> D[문서 생성]
    D --> E[의사결정]
    E --> F[실행]
    F --> G[검증]
```

## 💡 Best Practices

### DO
- ✅ 분석 목적을 명확히 정의
- ✅ 정량적 지표 포함
- ✅ 실행 가능한 제안 제시
- ✅ 이해관계자별 관점 고려

### DON'T
- ❌ 너무 기술적인 용어만 사용
- ❌ 근거 없는 추측
- ❌ 실행 계획 없는 비판
- ❌ 컨텍스트 없는 숫자

## 📊 효과 측정

### KPIs
- 문서 재사용률
- 의사결정 속도
- 실행 성공률
- 팀 만족도

### 월간 리뷰
- 생성된 분석 문서 수
- 실제 실행된 제안 비율
- 문서 품질 점수