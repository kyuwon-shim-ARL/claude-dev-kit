# Claude Code Development Best Practices

## 🎯 Core Principles

### 1. **키워드 기반 워크플로우**
간단한 한국어 키워드로 개발 단계를 명확히 구분:

#### 🔍 **"기획"** - Discovery & Planning Phase
- **포함**: 탐색 + 분석 + 계획 + PRD 작성 순환
- **동작**: 코드베이스 조사 → 문제 원인 분석 → 요구사항 정의 → 수렴까지 반복
- **완료 기준**: PRD 완성, 구현 방향 확정

#### ⚡ **"구현"** - Implementation Phase
- **포함**: TodoWrite 계획 + 코딩 + 단위 테스트 + 기본 검증
- **구현 원칙**:
  - ✅ **DRY (Don't Repeat Yourself)**: 기존 코드 검색 → 재사용 → 없으면 생성
  - ✅ **Single Source of Truth**: 동일 기능은 한 곳에만 구현
  - ✅ **Interface First**: 모듈 간 명확한 계약 정의
  - ✅ **Core Modules**: 공통 기능은 `core/` 디렉토리에 중앙화
- **구현 전 체크리스트**:
  - ☐ 비슷한 기능이 이미 있는가? (Grep/Search)
  - ☐ 재사용 가능한 유틸리티로 만들 수 있는가?
  - ☐ 이 코드를 수정할 때 다른 곳도 수정해야 하는가?
  - ☐ 테스트하기 쉬운 구조인가?
- **동작**: 계획 수립 → 기존 코드 검색 → 재사용/새로구현 → 테스트 작성
- **완료 기준**: 핵심 기능 동작 + 기본 테스트 통과 + 코드 중복 없음

#### 🔄 **"안정화"** - Validation & Polish Loop
- **포함**: 검증 → 문제발견 → 정리(리팩토링) → 재검증 순환 (수렴까지 반복)
- **1단계: 검증** - MECE 철저 테스트
  - ✅ 전체 기능 테스트 (엣지 케이스 포함)
  - ✅ 성능 측정 및 이전 버전 비교
  - ✅ MECE 방식 근거 검증 (구조적 완전성)
  - ✅ 코드 품질 점검 (스타일, 복잡도, 보안)
  - ✅ 에러 핸들링 및 복구 시나리오 테스트
- **2단계: 문제 발견 및 분석**
  - ✅ 성능 병목, 메모리 누수, 예외 처리 이슈 식별
  - ✅ 코드 녹냄새, 중복, 복잡도 문제 파악
  - ✅ 아키텍처 개선 포인트 도출
- **3단계: 정리(리팩토링)**
  - ✅ 성능 최적화 (알고리즘, 데이터 구조 개선)
  - ✅ 코드 구조 정리 (함수 분리, 모듈화, 중복 제거)
  - ✅ 네이밍 및 문서화 개선
  - ✅ 에러 핸들링 강화
  - ✅ 의존성 정리 및 인터페이스 단순화
- **4단계: 재검증**
  - ✅ 리팩토링 후 전체 기능 정상 동작 확인
  - ✅ 성능 개선 효과 측정
  - ✅ 새로운 버그 도입 여부 검사
- **순환 조건**: 2-4단계를 문제가 더 이상 발견되지 않을 때까지 반복
- **수렴 기준**: 모든 테스트 통과 + 성능 목표 달성 + 코드 품질 기준 충족

#### 🚀 **"배포"** - Deployment Phase
- **포함**: 최종 검증 + 커밋 + 푸시 + 태깅 (필요시)
- **자동 프로토콜**:
  - ✅ 배포 전 최종 체크리스트 실행
  - ✅ 의미있는 커밋 메시지 구조화 생성
  - ✅ 변경사항 영향도 분석
  - ✅ 버전 관리 및 태깅 검토
- **완료 기준**: 원격 저장소 반영, 배포 로그 기록

### 2. **TodoWrite 중심 개발**
```python
# 모든 복합 작업은 TodoWrite로 추적
todos = [
    {"content": "기획: 요구사항 분석 + PRD 작성", "status": "in_progress", "id": "001"},
    {"content": "구현: 핵심 기능 + 단위 테스트", "status": "pending", "id": "002"}, 
    {"content": "안정화: MECE 검증 + 품질 확보", "status": "pending", "id": "003"},
    {"content": "배포: 최종 검증 + 커밋&푸시", "status": "pending", "id": "004"}
]
```

### 3. **MECE 기반 진행률 추적**
- **Mutually Exclusive**: 중복 없는 작업 분할
- **Collectively Exhaustive**: 모든 범위 포함
- **정량적 평가**: "90% 완료" → "3/4 주요 기능 완료, 1개 이슈 남음"

## 📁 Project Structure Standards

### Essential Root Files Only
```
# ✅ 루트에 있어야 하는 것들
├── main_app.py        # 메인 애플리케이션 (배포 진입점)
├── test_setup.py      # 시스템 검증 (설치 진입점)
├── CLAUDE.md          # 프로젝트 문서 (개발 진입점)
├── README.md          # 기본 설명서
└── pyproject.toml     # 빌드 설정

# ❌ 루트에서 제거해야 하는 것들
├── internal_module.py    → src/project/
├── utility_script.py    → tools/
├── test_feature.py      → tests/
├── experiment.py        → examples/ or archive/
└── session_notes.md     → docs/development/
```

### Directory Categories
- **src/**: 핵심 구현체 (재사용 가능한 모듈)
- **core_features/**: 검증된 기능 (독립 실행 가능)
- **tools/**: 독립 유틸리티 (CLI 도구 등)
- **examples/**: 사용법 예제 (학습/데모용)
- **tests/**: 모든 테스트 코드
- **archive/**: 정리된 레거시 코드

## 💡 Development Workflows

### Session Start Pattern
```
1. "현재 상태 파악해줘" 또는 "이제 다음은 뭐야?"
2. TodoWrite로 작업 계획 수립
3. 우선순위에 따라 단계별 실행
4. 각 단계 완료 시 즉시 status 업데이트
```

### Commit Message Template
```
🎯 [Type] Brief summary of what was accomplished

## Major Changes
- **Added**: New functionality description
- **Fixed**: Bug fixes and corrections  
- **Organized**: Structural improvements
- **Updated**: Documentation and configuration changes

## Technical Details
- Specific implementation notes
- Important decisions made
- Files affected and why

## Impact
- How this affects the project
- What becomes possible now
- What problems this solves

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Documentation Standards
1. **CLAUDE.md**: Always current, single source of truth
2. **Session Archives**: docs/development/conversations/YYYY-MM-DD/
3. **Progress Tracking**: docs/CURRENT/PROJECT_STATUS.md
4. **Decision Records**: docs/development/guides/

## 🔧 Technical Standards

### Import Path Strategy
```python
# ✅ 좋은 패턴
from src.project.core.module import ClassName
from core_features.feature_name import FeatureClass

# ❌ 피해야 할 패턴  
from ../../../some_module import SomeThing
sys.path.append('random_path')
```

### Error Handling Philosophy
```python
# 실패 시 명확한 에러 메시지와 다음 단계 제시
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    print("❌ Issue identified: [clear description]")
    print("🔧 Next step: [specific action needed]")
    return None
```

### Testing Approach
```python
# 단위 테스트: 개별 함수/클래스
def test_specific_function():
    assert function_works_correctly()

# 통합 테스트: 전체 워크플로우  
def test_end_to_end_workflow():
    result = complete_process()
    assert result.meets_expectations()

# 설정 검증: 환경 및 의존성
def test_setup_requirements():
    assert all_dependencies_available()
```

## 🚀 New Repository Setup Checklist

### Initial Setup
- [ ] Run `python setup_claude_code_structure.py [project_name]`
- [ ] Customize CLAUDE.md with project details
- [ ] Configure .env file from .env.example
- [ ] Run `python test_setup.py` to verify setup
- [ ] Create initial git commit with full structure

### Development Environment
- [ ] Set up TodoWrite workflow patterns
- [ ] Configure documentation templates
- [ ] Establish testing framework
- [ ] Create example usage scripts
- [ ] Set up CI/CD if needed

### Team Onboarding
- [ ] Share CLAUDE.md as single source of truth
- [ ] Establish session archiving workflow
- [ ] Define commit message standards
- [ ] Set up progress tracking methods

## 📋 Session Templates

### Planning Session
```
목표: [명확한 목표 설정]
현황: [현재 상태 파악]
할일: [TodoWrite로 작업 분할]
우선순위: [중요도/긴급도 매트릭스]
```

### Implementation Session  
```
작업: [구체적 구현 내용]
진행: [실시간 상태 업데이트]
이슈: [발생한 문제와 해결책] 
검증: [테스트 및 확인 방법]
```

### Review Session
```
완료: [달성한 내용 정리]
학습: [얻은 인사이트]
다음: [후속 작업 계획]
아카이브: [세션 기록 정리]
```

이 방식을 따르면 어떤 새로운 프로젝트에서도 동일한 효율성과 체계성을 유지할 수 있습니다.