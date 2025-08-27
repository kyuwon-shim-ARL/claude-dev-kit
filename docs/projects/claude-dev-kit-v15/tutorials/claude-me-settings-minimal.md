# Claude.me 설정 (백업/고급 옵션)

> ⚠️ **주의**: 이 설정은 Claude Code를 사용할 수 없는 특수 상황에서만 사용하세요.
> 
> 🎯 **권장**: Claude Code + 슬래시 명령어 (/.전체사이클, /기획, /구현, /안정화, /배포)

## 🔧 언제 이 설정을 사용하나요?

**✅ 다음 상황에서만 사용:**
- 웹 claude.ai에서만 작업 가능한 경우
- Claude Code 설치가 불가능한 환경
- 프로젝트 외부에서 간단한 컨설팅/조언 시
- 키워드 기반 자연어 접근을 선호하는 경우

**❌ 다음 상황에서는 사용하지 마세요:**
- Claude Code가 설치 가능한 경우 → 슬래시 명령어 사용
- 정식 프로젝트 개발 시 → /전체사이클 사용
- 체계적 워크플로우가 필요한 경우 → Claude Code 우선

## ⚙️ 웹사이트에서 설정하는 방법:

1. https://claude.ai 접속
2. 우측 상단 프로필 → Settings
3. "Custom Instructions" 섹션
4. 아래 내용을 복사해서 붙여넣기

---

## 📝 Claude.me에 추가할 내용:

### Claude Code Workflow (Korean Keywords)
When user uses these keywords, IMMEDIATELY apply corresponding workflows:

- **"기획"** → **STRUCTURED DISCOVERY-PLANNING LOOP**:
  1. Discovery: Full codebase structure analysis, As-Is/To-Be/Gap identification
  2. Planning: MECE work breakdown (WBS), priority matrix, feasibility check
  3. Convergence: Discovery↔Planning iteration until PRD complete & consistent
  4. TodoWrite structuring with MECE principles

- **"구현"** → **IMPLEMENTATION WITH DRY**:
  1. Existing code search: Grep/Glob tools for similar functionality
  2. Reuse priority: Leverage existing libraries/modules/functions
  3. Create if needed: Develop new components with reusability in mind
  4. Quality assurance: Unit tests, basic validation, functionality check

- **"안정화"** → **STRUCTURAL SUSTAINABILITY PROTOCOL**:
  1. Repository structure scan: Analyze directory structure, file purposes
  2. Structural optimization: Logical grouping, hierarchy optimization
  3. Dependency resolution: Fix imports, resolve circular references
  4. User-centric testing: PRD-based real scenario testing (NO MOCKS)
  5. Documentation sync: Update CLAUDE.md, README, .gitignore
  6. Quality assurance: MECE analysis, performance benchmarks

- **"배포"** → **DEPLOYMENT**:
  1. Final validation: Checklist completion, test passing
  2. Structured commit: Meaningful commit messages, atomic changes
  3. Remote deployment: MANDATORY git push to remote repository
  4. Post-deployment verification: Remote repo access, endpoint testing

### Mock Test Prohibition
NEVER use mock data or fake testing. Always use real data and actual user scenarios.

### DRY Principle
Before creating new code, always search for existing similar functionality first.

### Quantitative Verification
Never say "passed" - always provide specific metrics and measurements.

---

## 💡 참고 사항

**이 설정은 Claude Code의 완전한 대체품이 아닙니다.**
- 슬래시 명령어만큼 정확하지 않음
- 프로젝트 컨텍스트 자동 로딩 없음
- 버전 관리 및 동기화 기능 없음

**최상의 경험을 위해서는 Claude Code를 설치하세요:**
```bash
# Claude Code 설치 후
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/init.sh | bash
```