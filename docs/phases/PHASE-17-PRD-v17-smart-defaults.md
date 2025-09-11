<!--
@meta
id: phase_20250905_1110_PHASE-17-PRD-v17-smart-defaults
type: phase
scope: tactical
status: archived
created: 2025-09-05
updated: 2025-09-09
tags: PRD, smart, defaults, PHASE, PHASE-17-PRD-v17-smart-defaults.md
related: 
-->

# PRD v17.0: Smart Defaults for Timeline Tracking

## Executive Summary
Git 저장소를 자동으로 감지하여 시간 추적을 스마트하게 활성화하고, 환경변수 지원 및 고급 리포팅 기능을 추가하여 사용성을 극대화

## Goals
1. **자동 감지**: Git 저장소에서는 자동으로 추적 활성화
2. **환경변수**: `CLAUDE_TRACK_CHANGES`로 전역 설정
3. **고급 리포팅**: 시각화, 통계, 트렌드 분석

## Requirements

### Phase 2: Smart Defaults (v17.0)

#### Git Detection
```python
def should_track_automatically():
    # 1. 환경변수 확인
    if os.getenv('CLAUDE_TRACK_CHANGES') == 'true':
        return True
    
    # 2. Git 저장소 확인
    if is_git_repository():
        return True
    
    # 3. 설정 파일 확인
    if has_tracking_config():
        return True
    
    return False
```

#### Advanced Reporting
- 변경 트렌드 그래프
- 파일별 수정 빈도 히트맵
- 코드-문서 연동 시각화
- 팀 협업 통계

### Implementation Details

#### 1. Smart Detection Module
```python
class SmartTracker:
    def __init__(self):
        self.auto_track = self._detect_tracking_mode()
    
    def _detect_tracking_mode(self):
        # Priority order:
        # 1. Explicit parameter (--track/--no-track)
        # 2. Environment variable
        # 3. Git repository detection
        # 4. Config file
        # 5. Default (false)
```

#### 2. Enhanced Reports
```markdown
## 📊 Timeline Analytics Report

### Change Velocity
- Daily average: 4.2 changes
- Peak time: 14:00-16:00
- Most active day: Wednesday

### File Hotspots
```
src/core/    ████████████ 45%
docs/        ███████      28%
tests/       ████         15%
scripts/     ███          12%
```

### Collaboration Metrics
- Contributors: 3
- Average PR cycle: 2.3 days
- Code-to-doc ratio: 3:1
```

## Success Metrics
- Auto-detection accuracy: >95%
- Report generation time: <3s
- User satisfaction: >80%

## Timeline
- Week 1: Git detection & env variable
- Week 2: Advanced reporting
- Week 3: Testing & optimization