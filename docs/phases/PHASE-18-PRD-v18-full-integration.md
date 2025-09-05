<!--
@meta
id: phase_20250905_1110_PHASE-18-PRD-v18-full-integration
type: phase
scope: tactical
status: archived
created: 2025-09-05
updated: 2025-09-05
tags: PRD, v18, full, PHASE, integration
related: 
-->

# PRD v18.0: Full Integration - Default Timeline Tracking

## Executive Summary
시간 추적을 기본 동작으로 설정하고, 레거시 모드를 통해 하위 호환성을 유지하는 완전 통합 시스템

## Background
- **Phase 1 (v16.0)**: 옵트인 파라미터 (`--track`) ✅
- **Phase 2 (v17.0)**: 스마트 기본값 (Git 감지) ✅  
- **Phase 3 (v18.0)**: 기본값으로 시간 추적 (이번 구현)

## Goals
1. **기본 추적**: 모든 명령어에서 기본적으로 시간 추적
2. **레거시 지원**: `--no-track`, `--legacy` 옵션
3. **완전한 분석**: 고급 통계, 트렌드, 예측

## Requirements

### Phase 3: Full Integration (v18.0)

#### Default Behavior Change
```python
def _should_track(self, args: List[str], force_track: bool = None) -> Tuple[bool, str]:
    """v18.0: Default to tracking unless explicitly disabled"""
    # Priority 1: Explicit disable
    if "--no-track" in args or "--legacy" in args:
        return False, "explicit disable parameter"
    
    # Priority 2: Environment disable
    if os.getenv('CLAUDE_TRACK_CHANGES', '').lower() == 'false':
        return False, "environment variable CLAUDE_TRACK_CHANGES=false"
    
    # Default: Always track (v18.0)
    return True, "default behavior (v18.0)"
```

#### Legacy Mode Support
```bash
# 구버전 동작 (추적 없음)
/레포정리 --legacy
/레포정리 --no-track

# 새 기본 동작 (항상 추적)
/레포정리  # 자동 추적
```

#### Advanced Analytics
- **트렌드 분석**: 주/월별 변화 패턴
- **성능 예측**: 코드 변경 속도 예측
- **팀 분석**: 기여자별 패턴
- **품질 지표**: 변경 복잡도, 안정성

### Implementation Plan

#### Week 1: Core Changes
- [ ] 기본 동작을 추적으로 변경
- [ ] `--no-track`, `--legacy` 파라미터 추가
- [ ] 환경변수 `=false` 지원

#### Week 2: Advanced Features
- [ ] 트렌드 분석 알고리즘
- [ ] 예측 모델 구현
- [ ] 시각화 개선

#### Week 3: Testing & Migration
- [ ] 마이그레이션 가이드
- [ ] 하위 호환성 테스트
- [ ] 성능 벤치마크

## Breaking Changes
- **기본 동작 변경**: v16-17에서는 옵트인, v18부터 기본값
- **마이그레이션**: 기존 사용자는 `CLAUDE_TRACK_CHANGES=false` 설정 가능

## Success Criteria
- [ ] 100% 하위 호환성 유지
- [ ] 성능 영향 < 5%
- [ ] 고급 분석 정확도 > 90%