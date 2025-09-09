<!--
@meta
id: document_20250905_1110_project-based-documentation
type: document
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-05
tags: project-based-documentation.md, claude-dev-kit-v10, projects, 06-documentation, project
related: 
-->

# PRD: 연구 프로젝트 중심 문서 관리 시스템

## 1. 핵심 문제
"해석, 보고서, 비교는 이미 Claude가 잘 해주는데, **어느 프로젝트의 문서인지 체계적으로 관리가 안 됨**"

## 2. 해결 방안

### 2.1 프로젝트 초기화 명령어
```bash
/프로젝트시작 "2024-RNA-seq-drug-response"
```

자동으로 생성되는 구조:
```
projects/2024-RNA-seq-drug-response/
├── README.md           # 프로젝트 개요 (자동 생성)
├── .project            # 프로젝트 메타데이터
├── roadmap.md          # 연구 로드맵 템플릿
├── 01-hypothesis/      # 가설 및 배경
├── 02-design/          # 실험 설계
├── 03-data/            # 원시 데이터
├── 04-analysis/        # 분석 결과
├── 05-validation/      # 검증
├── 06-manuscript/      # 논문/보고서
└── timeline.md         # 진행 상황
```

### 2.2 현재 프로젝트 설정
```bash
/프로젝트선택 "2024-RNA-seq-drug-response"
# 또는 자동 감지 (현재 디렉토리 기반)
```

### 2.3 기존 명령어 자동 연동
```bash
# 프로젝트가 선택된 상태에서
/분석 "DEG 분석 결과"
→ 자동으로 projects/2024-RNA-seq-drug-response/04-analysis/에 저장

/보고서 "중간 보고서"
→ 자동으로 projects/2024-RNA-seq-drug-response/06-manuscript/에 저장
```

## 3. 실제 사용 시나리오

### 시나리오 1: 새 프로젝트 시작
```bash
# 1. 프로젝트 초기화
/프로젝트시작 "2024-biomarker-discovery"

# 2. 가설 문서화
/기획 "혈액 단백질 바이오마커로 조기 진단 가능성 탐색"
→ projects/2024-biomarker-discovery/01-hypothesis/initial-hypothesis.md

# 3. 실험 설계
/기획 "100명 환자군 vs 100명 대조군 프로테오믹스"
→ projects/2024-biomarker-discovery/02-design/experimental-design.md
```

### 시나리오 2: 진행 중인 프로젝트
```bash
# 1. 프로젝트 상태 확인
/프로젝트상태
→ "현재: 04-analysis 단계, 3개 분석 완료"

# 2. 분석 수행 및 자동 저장
python run_analysis.py
/분석 "results.csv 해석"
→ projects/current/04-analysis/2024-01-26-results-interpretation.md

# 3. 이전 분석과 비교
/비교 "1월 15일 vs 1월 26일 결과"
→ projects/current/04-analysis/comparison-jan15-vs-jan26.md
```

### 시나리오 3: 프로젝트 전체 보기
```bash
/프로젝트요약
→ 로드맵 진행률, 문서 트리, 주요 마일스톤 표시
```

## 4. 핵심 차별점

### 기존 방식 (날짜/기능 중심)
```
docs/analysis/2024-01-26-degs.md          # 어느 프로젝트?
docs/reports/2024-01-27-report.md         # 뭐에 대한 보고서?
docs/analysis/2024-01-28-pathway.md       # 관련성?
```

### 새로운 방식 (프로젝트 중심)
```
projects/drug-response/
├── 04-analysis/
│   ├── degs.md
│   ├── pathway.md
│   └── comparison.md
└── 06-manuscript/
    └── draft-v1.md
```
→ 한 눈에 프로젝트 전체 스토리 파악 가능

## 5. 구현 우선순위

### P0 (즉시 필요)
- [ ] /프로젝트시작 명령어
- [ ] 프로젝트 폴더 구조 자동 생성
- [ ] 현재 프로젝트 컨텍스트 관리

### P1 (다음 단계)
- [ ] 기존 명령어와 자동 연동
- [ ] 프로젝트 상태 추적
- [ ] 로드맵 진행률 표시

### P2 (향후 개선)
- [ ] 다중 프로젝트 관리
- [ ] 프로젝트 간 지식 공유
- [ ] 자동 아카이빙

## 6. 기대 효과

1. **체계적 관리**: 프로젝트별로 모든 문서가 한 곳에
2. **쉬운 추적**: 연구 진행 상황 한눈에 파악
3. **재사용성**: 이전 프로젝트 참조 용이
4. **협업 개선**: 팀원들이 프로젝트 구조 쉽게 이해

## 7. 메타데이터 예시 (.project 파일)
```yaml
name: "2024-RNA-seq-drug-response"
type: "transcriptomics"
status: "analysis"
created: "2024-01-15"
pi: "Dr. Kim"
current_stage: "04-analysis"
milestones:
  - hypothesis: complete
  - design: complete
  - data_collection: complete
  - analysis: in_progress
  - validation: pending
  - manuscript: pending
```

---
*이 시스템의 핵심은 "프로젝트 컨텍스트 유지"입니다. 
모든 작업이 현재 선택된 프로젝트 안에서 자동으로 정리됩니다.*