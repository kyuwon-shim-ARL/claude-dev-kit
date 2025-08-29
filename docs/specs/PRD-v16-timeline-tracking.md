# PRD v16.0: Timeline Tracking System for Commands

## Executive Summary
시간 추적 기능을 `/레포정리`, `/문서정리` 명령어에 추가하여 코드 변경 이력, 문서 생성 과정, 피드백 루프를 체계적으로 관리하는 시스템 구축

## Background
- **문제**: 현재 명령어들은 단순 정리만 수행하고, 언제/무엇이/왜 변경되었는지 추적 불가
- **영향**: 프로젝트 진화 과정 추적 불가, 의사결정 근거 소실, 피드백 루프 단절

## Goals & Success Metrics

### Primary Goals
1. 모든 변경사항에 타임스탬프 기록
2. 코드 변경과 문서 생성 간 인과관계 추적
3. 피드백 → PRD 반영 사이클 가시화

### Success Metrics
- 변경 이력 캡처율: 95% 이상
- 리포트 생성 시간: 5초 이내
- 사용자 채택률: 60% (Phase 1)

## Requirements

### Functional Requirements

#### Phase 1: Opt-in Parameter (v16.0)
```bash
/레포정리 --track
/문서정리 --with-timeline
```

**Features:**
- `--track` 파라미터 추가
- `.claude/tracking/` 디렉토리 생성
- JSON 기반 메타데이터 저장
- 기본 리포트 생성

#### Phase 2: Smart Defaults (v17.0)
```bash
# Git 저장소면 자동 추적
/레포정리  # 자동 --track
```

**Features:**
- Git 감지 로직
- 환경변수 지원 (`CLAUDE_TRACK_CHANGES`)
- 고급 리포팅 (그래프, 통계)

#### Phase 3: Full Integration (v18.0)
```bash
# 기본값으로 시간 추적
/레포정리  # 항상 추적
/레포정리 --no-track  # 명시적 비활성화
```

### Non-Functional Requirements
- **Performance**: 추적 오버헤드 < 200ms
- **Storage**: 메타데이터 < 1MB/month
- **Compatibility**: 하위 호환성 100% 유지

## Technical Design

### Data Structure
```json
{
  "version": "1.0",
  "tracking": {
    "id": "tr-2024-08-29-001",
    "timestamp": "2024-08-29T10:30:00Z",
    "command": "레포정리",
    "parameters": ["--track"],
    "git": {
      "commit": "abc123",
      "branch": "main",
      "author": "user@example.com"
    },
    "changes": {
      "files_modified": 12,
      "lines_added": 245,
      "lines_removed": 89
    },
    "generated": {
      "reports": ["timeline-report.md"],
      "metadata": ["tracking.json"]
    },
    "duration_ms": 3240
  }
}
```

### Directory Structure
```
.claude/
├── tracking/
│   ├── history.json       # 전체 이력
│   ├── 2024-08/          # 월별 아카이브
│   │   ├── week-35.json
│   │   └── summary.md
│   └── current.json      # 현재 세션
└── reports/
    ├── timeline/         # 시간축 리포트
    └── dependency/       # 의존성 그래프
```

## Implementation Plan

### Week 1: Infrastructure
- [ ] `.claude/tracking/` 구조 생성
- [ ] JSON 스키마 정의
- [ ] Git 연동 유틸리티

### Week 2: Command Integration
- [ ] `--track` 파라미터 파싱
- [ ] 메타데이터 수집 로직
- [ ] 저장 및 검색 기능

### Week 3: Reporting
- [ ] Timeline 리포트 생성
- [ ] 변경 통계 계산
- [ ] Markdown 포맷팅

### Week 4: Testing & Polish
- [ ] 단위 테스트
- [ ] 통합 테스트
- [ ] 문서화

## Risks & Mitigation

### Risk 1: Performance Impact
- **Mitigation**: 비동기 처리, 캐싱

### Risk 2: Storage Growth
- **Mitigation**: 자동 아카이빙, 압축

### Risk 3: User Adoption
- **Mitigation**: 점진적 도입, 명확한 이점 제시

## Success Criteria
- [ ] Phase 1 구현 완료
- [ ] 테스트 커버리지 > 80%
- [ ] 문서화 100% 완료
- [ ] 성능 목표 달성

## Timeline
- **Week 1-2**: Phase 1 개발
- **Week 3**: 테스트 및 안정화
- **Week 4**: 배포 및 모니터링

## Appendix
- 사용자 시나리오
- API 명세
- 예제 리포트