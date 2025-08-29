# Architecture Specification (Extracted from v16)
Generated: 2025-08-29 11:26:46

## System Overview

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

## Component Architecture

### Core Components
- **Command Processor**: Handles user input and routing
- **Tracking Manager**: Manages timeline and metadata
- **Report Generator**: Creates analysis and reports
- **Configuration Manager**: Handles settings and preferences


## Data Flow
- Input: User commands and parameters
- Processing: Version-specific logic routing
- Storage: JSON-based metadata persistence
- Output: Enhanced reports and analytics

## Integration Points
- Git repository integration
- Environment variable configuration
- File system metadata storage
- Command parameter processing

---
*Extracted from v16 PRD. See full PRD for implementation details.*

---

# v17 Addition

# Architecture Specification (Extracted from v17)
Generated: 2025-08-29 11:26:46

## System Overview

Details

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

## Component Architecture

### Core Classes
- **SmartTracker**: Core component for system functionality


## Data Flow
- Input: User commands and parameters
- Processing: Version-specific logic routing
- Storage: JSON-based metadata persistence
- Output: Enhanced reports and analytics

## Integration Points
- Git repository integration
- Environment variable configuration
- File system metadata storage
- Command parameter processing

---
*Extracted from v17 PRD. See full PRD for implementation details.*

---

# v18 Addition

# Architecture Specification (Extracted from v18)
Generated: 2025-08-29 11:26:46

## System Overview

Plan

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

## Component Architecture

### Core Components
- **Command Processor**: Handles user input and routing
- **Tracking Manager**: Manages timeline and metadata
- **Report Generator**: Creates analysis and reports
- **Configuration Manager**: Handles settings and preferences


## Data Flow
- Input: User commands and parameters
- Processing: Version-specific logic routing
- Storage: JSON-based metadata persistence
- Output: Enhanced reports and analytics

## Integration Points
- Git repository integration
- Environment variable configuration
- File system metadata storage
- Command parameter processing

---
*Extracted from v18 PRD. See full PRD for implementation details.*

---

# v16 Addition

# Architecture Specification (Extracted from v16)
Generated: 2025-08-29 11:28:21

## System Overview

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

## Component Architecture

### Core Components
- **Command Processor**: Handles user input and routing
- **Tracking Manager**: Manages timeline and metadata
- **Report Generator**: Creates analysis and reports
- **Configuration Manager**: Handles settings and preferences


## Data Flow
- Input: User commands and parameters
- Processing: Version-specific logic routing
- Storage: JSON-based metadata persistence
- Output: Enhanced reports and analytics

## Integration Points
- Git repository integration
- Environment variable configuration
- File system metadata storage
- Command parameter processing

---
*Extracted from v16 PRD. See full PRD for implementation details.*

---

# v17 Addition

# Architecture Specification (Extracted from v17)
Generated: 2025-08-29 11:28:21

## System Overview

Details

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

## Component Architecture

### Core Classes
- **SmartTracker**: Core component for system functionality


## Data Flow
- Input: User commands and parameters
- Processing: Version-specific logic routing
- Storage: JSON-based metadata persistence
- Output: Enhanced reports and analytics

## Integration Points
- Git repository integration
- Environment variable configuration
- File system metadata storage
- Command parameter processing

---
*Extracted from v17 PRD. See full PRD for implementation details.*

---

# v18 Addition

# Architecture Specification (Extracted from v18)
Generated: 2025-08-29 11:28:21

## System Overview

Plan

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

## Component Architecture

### Core Components
- **Command Processor**: Handles user input and routing
- **Tracking Manager**: Manages timeline and metadata
- **Report Generator**: Creates analysis and reports
- **Configuration Manager**: Handles settings and preferences


## Data Flow
- Input: User commands and parameters
- Processing: Version-specific logic routing
- Storage: JSON-based metadata persistence
- Output: Enhanced reports and analytics

## Integration Points
- Git repository integration
- Environment variable configuration
- File system metadata storage
- Command parameter processing

---
*Extracted from v18 PRD. See full PRD for implementation details.*

---

# v19 Addition

# Architecture Specification (Extracted from v19)
Generated: 2025-08-29 11:28:21

## System Overview

### Architecture Components
```python
class SpecsManager:
    def extract_requirements(self, prd_content):
        # Extract all requirements automatically
        return consolidated_requirements
    
    def extract_architecture(self, prd_content):
        # Extract system design automatically  
        return architectural_specs
```

### Data Structure
```json
{
  "specs": {
    "requirements": "docs/specs/requirements.md",
    "architecture": "docs/specs/architecture.md", 
    "project_rules": "docs/specs/project_rules.md"
  },
  "session": {
    "planning": "docs/CURRENT/session-planning.md",
    "todos": "docs/CURRENT/active-todos.md"
  }
}
```

## Component Architecture

### Core Classes
- **SpecsManager**: Core component for system functionality


## Data Flow
- Input: User commands and parameters
- Processing: Version-specific logic routing
- Storage: JSON-based metadata persistence
- Output: Enhanced reports and analytics

## Integration Points
- Git repository integration
- Environment variable configuration
- File system metadata storage
- Command parameter processing

---
*Extracted from v19 PRD. See full PRD for implementation details.*