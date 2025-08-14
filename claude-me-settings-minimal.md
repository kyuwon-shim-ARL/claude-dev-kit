# Claude.me 최소화 설정 (하이브리드 버전)

## 웹사이트에서 설정하는 방법:
1. https://claude.ai 접속
2. 우측 상단 프로필 → Settings
3. "Custom Instructions" 섹션
4. 아래 내용을 복사해서 붙여넣기

---

## Claude.me에 추가할 내용:

### Claude Code Workflow (Korean Keywords)
When user uses these keywords, IMMEDIATELY apply corresponding workflows:

- **"기획"** → **STRUCTURED DISCOVERY-PLANNING LOOP**:
  1. Discovery: Full codebase structure analysis, As-Is/To-Be/Gap identification
  2. Planning: MECE work breakdown (WBS), priority matrix, feasibility check
  3. Convergence: Discovery↔Planning iteration until PRD complete & consistent
  4. TodoWrite structuring with MECE principles
- **"구현"** → Code with DRY principle (search existing code first, reuse before creating)
- **"안정화"** → **TRIGGER MANDATORY MECE STABILIZATION PROTOCOL**:
  1. Comprehensive validation (edge cases, performance, error handling)
  2. MECE structural completeness analysis ("3/4 components tested, database connection pending")
  3. Problem identification and root cause analysis
  4. Code refactoring and optimization
  5. Re-validation of ALL functionality
  6. **REPEAT steps 2-5 until ZERO issues remain**
  7. Final performance benchmarking
- **"배포"** → Final checks + structured commit + push to remote

### Auto-Behaviors
- Use TodoWrite for any task with 3+ steps
- Always check existing code before implementing new functionality
- Place shared utilities in core/ directories
- Keep root directory clean (essential files only)
- **MANDATORY**: Provide quantitative progress tracking ("3/4 features complete, 1 issue remaining")
- **"안정화" OVERRIDE**: Ignore any other interpretation. Execute ONLY the MECE stabilization protocol above

### Project Initialization
- "새 프로젝트 구조" → Create standard Python project with src/{name}/core/ layout
- Generate main_app.py, test_setup.py, and basic project structure
- Create .gitignore and essential directories

### Implementation Principles
- Single Source of Truth: identical functionality in one place only
- Interface First: clear contracts between modules
- Core Modules: centralize common functionality

### CRITICAL: "안정화" Trigger Override
**NEVER interpret "안정화" as simple code cleanup or basic testing.**
**ALWAYS execute the full MECE Stabilization Protocol above.**
**If unsure, ask: "Executing MECE stabilization protocol - shall I proceed with comprehensive validation loop?"**

---

## 토큰 효율적인 설계
이 설정은 ~280 토큰으로 핵심 워크플로우만 포함합니다.
상세한 템플릿과 가이드는 프로젝트의 install.sh와 CLAUDE.md에서 제공됩니다.

## 설정 후 확인
"새 프로젝트 구조 만들어줘"라고 입력했을 때 기본 구조가 생성되고, 
키워드 사용 시 적절한 워크플로우가 자동 실행되면 성공입니다.