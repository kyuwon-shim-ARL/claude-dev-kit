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
- **"안정화"** → **TRIGGER MANDATORY STRUCTURAL SUSTAINABILITY PROTOCOL v2.0**:
  1. **Repository Structure Scan**: Full file analysis, duplicate detection, dependency mapping
  2. **Structural Optimization**: File classification, directory hierarchy cleanup, naming standardization
  3. **Dependency Resolution**: Import path fixes, reference error resolution, environment sync
  4. **Comprehensive Testing**: All module imports, API functionality, system integrity validation
  5. **Documentation Sync**: CLAUDE.md update, README alignment, .gitignore cleanup
  6. **Quality Assurance**: MECE analysis, performance benchmarks, quantitative metrics
  7. **REPEAT steps 1-6 until ZERO structural + functional issues remain**
- **"배포"** → Final checks + structured commit + push to remote

### Auto-Behaviors
- Use TodoWrite for any task with 3+ steps
- Always check existing code before implementing new functionality
- Place shared utilities in core/ directories
- Keep root directory clean (essential files only)
- **MANDATORY**: Provide quantitative progress tracking ("3/4 features complete, 1 issue remaining")
- **"안정화" OVERRIDE**: Execute STRUCTURAL SUSTAINABILITY PROTOCOL v2.0 above
- **Auto-trigger conditions**: Root 20+ files, temp files 5+, import errors 3+, every 5th commit

### Project Initialization  
- "새 프로젝트 구조" → Create standard Python project with src/{name}/core/ layout
- Generate main_app.py and basic project structure with auto-validation
- Create .gitignore and essential directories
- Automatic system verification and cleanup

### Implementation Principles
- Single Source of Truth: identical functionality in one place only
- Interface First: clear contracts between modules
- Core Modules: centralize common functionality

### CRITICAL: "안정화" Trigger Override
**NEVER interpret "안정화" as simple code cleanup or basic testing.**
**ALWAYS execute the full STRUCTURAL SUSTAINABILITY PROTOCOL v2.0 above.**
**Priority: Repository structure + file organization BEFORE functional testing.**
**If unsure, ask: "Executing Structural Sustainability Protocol v2.0 - shall I proceed with 6-stage comprehensive validation?"**

---

## 토큰 효율적인 설계
이 설정은 ~280 토큰으로 핵심 워크플로우만 포함합니다.
상세한 템플릿과 가이드는 프로젝트의 install.sh와 CLAUDE.md에서 제공됩니다.

## 설정 후 확인  
curl 설치 시 자동 검증이 완료되고, 키워드 사용 시 워크플로우가 자동 실행되면 성공입니다.
"@기획", "@구현", "@안정화", "@배포" 키워드가 설계된 프로토콜대로 동작하는지 확인하세요.