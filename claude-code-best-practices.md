# Claude Code Development Best Practices

## 🎯 Core Principles

### 1. **키워드 기반 워크플로우**
간단한 한국어 키워드로 개발 단계를 명확히 구분:

#### 🔍 **"기획"** - Structured Discovery & Planning Loop
- **포함**: 체계적 탐색↔계획 수렴 루프
- **탐색 (Discovery)**:
  - ✅ 전체 코드베이스 구조 파악 (디렉토리, 의존성)
  - ✅ 현재 상태(As-Is) 철저 분석
  - ✅ 목표 상태(To-Be) 명확 정의
  - ✅ 갭(Gap) 식별 및 영향도 평가
- **계획 (Planning)**:
  - ✅ MECE 기반 작업 분해(WBS)
  - ✅ 우선순위 매트릭스 작성 (중요도/긴급도)
  - ✅ 실행 가능성 검증
  - ✅ 리스크 식별 및 대응 방안
- **수렴 (Convergence)**:
  - ✅ 탐색↔계획 반복 until 일관성 확보
  - ✅ PRD 문서화 완성
  - ✅ TodoWrite 구조화 (MECE 원칙)
- **완료 기준**: PRD 수렴 + 모든 이해관계자 동의

#### ⚡ **"구현"** - Implementation with DRY
- **포함**: DRY 원칙 기반 체계적 구현
- **구현 원칙**:
  - ✅ **DRY (Don't Repeat Yourself)**: 기존 코드 검색 → 재사용 → 없으면 생성
  - ✅ **Single Source of Truth**: 동일 기능은 한 곳에만 구현
  - ✅ **Interface First**: 모듈 간 명확한 계약 정의
  - ✅ **Core Modules**: 공통 기능은 `core/` 디렉토리에 중앙화
- **구현 전 체크리스트**:
  - ☐ 비슷한 기능이 이미 있는가? (Grep/Search 필수)
  - ☐ core/ 디렉토리에 공통 유틸로 만들어야 하는가?
  - ☐ 이 코드를 수정할 때 다른 곳도 수정해야 하는가?
  - ☐ 인터페이스와 구현이 명확히 분리되었는가?
- **실행 프로세스**:
  1. TodoWrite 기반 작업 시작
  2. 기존 코드 철저 검색 (Grep/Glob)
  3. 재사용 또는 새로 구현 결정
  4. 단위 테스트 동시 작성
  5. 기본 검증 수행
- **완료 기준**: 기능 동작 + 테스트 통과 + 중복 제로 + 문서화

#### 🔄 **"안정화"** - Structural Sustainability Protocol v2.0
- **핵심**: 구조적 지속가능성 우선 → 기능적 완성도
- **패러다임**: 기능 중심에서 **전체 시스템 무결성** 중심으로 전환

**🔍 1단계: Repository Structure Scan**
  - ✅ 전체 파일 구조 스캔 및 분류 현황 파악
  - ✅ 중복/임시/불필요 파일 식별 (*.tmp, *.bak, 중복 등)
  - ✅ 의존성 맵핑 및 순환참조 검출
  - ✅ 구조적 문제점 정량화 ("루트 23개 파일, 중복 5건")

**🏗️ 2단계: Structural Optimization**
  - ✅ 파일 분류 및 적절한 디렉토리 이동
  - ✅ 계층구조 정리 (core/, services/, models/, tools/ 등)
  - ✅ 중복 파일 제거 및 통합
  - ✅ 네이밍 컨벤션 표준화

**🔧 3단계: Dependency Resolution**
  - ✅ Import 경로 자동 수정 (파일 이동 후)
  - ✅ 참조 오류 해결 및 검증
  - ✅ 환경 설정 동기화 (.env, requirements.txt 등)
  - ✅ 외부 의존성 정리 및 최적화

**✅ 4단계: Comprehensive Testing**
  - ✅ 모든 모듈 Import 검증 (순환참조 포함)
  - ✅ API 엔드포인트 기능 테스트
  - ✅ 파일 이동 후 시스템 무결성 확인
  - ✅ 성능 회귀 테스트 (구조 변경 영향도)
  - **🌐 웹 프로젝트 전용**: Playwright E2E 테스트 필수 실행
    - `./scripts/test-web.sh` 또는 `uv run pytest src/web/tests/`
    - 브라우저 렌더링, 사용자 플로우, API 통합 검증
    - 반응형 디자인 및 크로스 브라우저 호환성

**📝 5단계: Documentation Sync**
  - ✅ CLAUDE.md 구조 변경사항 반영
  - ✅ README.md 업데이트
  - ✅ .gitignore 정리 및 최적화
  - ✅ 변경사항 로그 및 마이그레이션 가이드 작성

**🎯 6단계: Quality Assurance**
  - ✅ 전체 기능 테스트 (엣지 케이스 포함)
  - ✅ 성능 측정 및 이전 버전 비교
  - ✅ MECE 방식 근거 검증 (구조적 완전성)
  - ✅ 코드 품질 점검 (스타일, 복잡도, 보안)
  - ✅ MECE 프로토콜 실행 (구조적 완전성)
  - ✅ 성능 벤치마크 비교 (구조 변경 전후)
  - ✅ 코드 품질 메트릭스 (복잡도, 중복도, 테스트 커버리지)
  - ✅ 완성도 정량 평가 ("6/6 단계 완료, 0건 이슈")

**🔄 순환 조건**: 
- 1-6단계를 **구조적 + 기능적 ZERO 이슈**까지 반복
- 우선순위: **Repository 구조 정리 → 기능 검증**
- 완료 기준: 파일 분류 완료 + 모든 테스트 통과 + 문서 동기화

**⚠️ 중요**: 기존 "기능 중심" 안정화에서 **"구조적 지속가능성"** 중심으로 패러다임 전환

**📋 예방적 관리 트리거**:
- 루트 디렉토리 파일 20개 이상
- 임시 파일 (.tmp, .bak) 5개 이상
- Import 오류 3개 이상 
- 매 5번째 커밋마다 자동 실행

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
├── scripts/test_setup.py      # 시스템 검증 (설치 진입점)
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
- [ ] Run `python scripts/test_setup.py` to verify setup
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