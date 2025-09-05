<!--
@meta
id: document_20250905_1110_command-priority-and-versioning
type: document
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-05
tags: priority, claude-dev-kit-v10, 03-implementation, projects, versioning
related: 
-->

# 명령어 우선순위 및 문서 버전 관리 가이드

## 1. 명령어 우선순위 체계

### 1.1 현재 Claude Code 동작
- 로컬(.claude/commands)과 글로벌(~/.claude/commands) 충돌 시 **명확한 우선순위 없음**
- 충돌 회피가 권장됨

### 1.2 실용적 해결책: 네임스페이스 방식

#### 글로벌 명령어 (범용)
```bash
~/.claude/commands/
├── 기획.md        # 모든 프로젝트에서 사용
├── 구현.md
├── 안정화.md
└── 배포.md
```

#### 프로젝트 명령어 (특화)
```bash
projects/rna-seq/.claude/commands/
├── rna-qc.md      # RNA-seq 특화 QC 명령
├── deg.md         # DEG 분석 특화
└── pathway.md     # Pathway 분석 특화
```

### 1.3 명령어 네이밍 컨벤션

**DO:**
- 프로젝트 특화: `/rna-분석`, `/proteome-qc`
- 명확한 구분: `/deg` (프로젝트), `/분석` (글로벌)

**DON'T:**
- 중복 이름: 프로젝트와 글로벌에 동일한 `/분석`
- 모호한 이름: `/처리`, `/실행`

## 2. 문서 버전 관리 체계

### 2.1 과하지 않은 실용적 접근

#### ❌ 너무 복잡 (비추천)
```
CURRENT/
├── draft.md
versions/
├── v0.1/
├── v0.2/
├── v1.0/
archive/
├── 2024-01/
└── 2024-02/
```
**문제**: 폴더 구조 복잡, 찾기 어려움, 관리 부담

#### ✅ 적절한 수준 (권장)
```
projects/drug-response/
├── manuscript.md           # 현재 작업 중
├── manuscript-v1.md        # 첫 번째 완성본
├── manuscript-review.md    # 리뷰 버전
└── manuscript-final.md     # 최종 제출본
```
**장점**: 단순, 명확, 히스토리 추적 가능

### 2.2 버전 관리 원칙

#### 언제 새 버전을 만들 것인가?
1. **마일스톤 달성 시**
   - 초안 완성 → manuscript-draft.md
   - 리뷰 완료 → manuscript-reviewed.md
   - 최종 승인 → manuscript-final.md

2. **주요 변경 전**
   - 대규모 수정 전 백업
   - 방향 전환 시점

3. **공유 시점**
   - 외부 공유 버전 고정
   - 협업자 피드백 버전

#### Git과의 조화
```bash
# Git이 세부 버전 관리
git log manuscript.md  # 모든 변경 이력

# 파일명은 주요 마일스톤만
manuscript-submitted.md  # 제출 버전 고정
```

## 3. 실제 적용 예시

### 시나리오: RNA-seq 프로젝트

```bash
# 1. 프로젝트 시작
/프로젝트시작 "rna-seq-2024"

# 2. 프로젝트 구조
projects/rna-seq-2024/
├── .claude/commands/
│   ├── deg.md          # DEG 분석 특화 명령
│   └── pathway.md      # Pathway 분석 특화
├── analysis/
│   ├── qc-report.md
│   ├── deg-results.md
│   └── deg-results-v1.md  # 첫 번째 분석 보존
└── manuscript/
    ├── draft.md            # 작업 중
    └── draft-advisor.md    # 지도교수 리뷰용
```

### 버전 진행 예시
```
draft.md (작업 중)
↓ 완성
draft-v1.md (백업) + draft.md (계속 수정)
↓ 리뷰
draft-reviewed.md (리뷰 반영)
↓ 최종
manuscript-nature.md (투고본)
```

## 4. 결론 및 권장사항

### DO ✅
1. **명령어**: 프로젝트별 고유 네임스페이스 사용
2. **버전**: 주요 마일스톤만 파일명으로 구분
3. **Git**: 세부 버전 관리는 Git에 위임
4. **단순함**: CURRENT 폴더 없이도 충분

### DON'T ❌
1. **명령어**: 글로벌과 로컬에 같은 이름 사용
2. **버전**: 모든 수정마다 새 버전 파일
3. **복잡도**: versions/, archive/ 등 과도한 구조
4. **중복**: Git과 파일명 버전 중복 관리

### 핵심 원칙
> "복잡도는 필요에 따라 점진적으로 증가시키되,
> 처음부터 과도한 구조를 만들지 말자"

---
*실용성과 체계성의 균형이 핵심입니다.*