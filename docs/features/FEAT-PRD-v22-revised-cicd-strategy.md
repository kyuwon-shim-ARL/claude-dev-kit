<!--
@meta
id: strategy_20250905_1110_FEAT-PRD-v22-revised-cicd-strategy
type: strategy
scope: strategic
status: archived
created: 2025-09-05
updated: 2025-09-05
tags: PRD, FEAT-PRD-v22-revised-cicd-strategy.md, v22, cicd, FEAT
related: 
-->

# PRD v22 개정: Claude-dev-kit 맞춤형 CI/CD 전략

## 🎯 전략 재정의

### nf-core 사례 분석 결과
**장점 (채택 가능)**
- PR 기반 자동 테스트 ✅
- 태그 기반 버전 관리 ✅
- 단계별 품질 게이트 ✅

**차이점 (적용 불가)**
- Nextflow Tower 의존 ❌ → Claude-dev-kit은 로컬 실행
- HPC/클라우드 배포 ❌ → 개발자 로컬 환경
- 데이터 파이프라인 ❌ → 개발 도구 설치

## 📋 Claude-dev-kit 특화 CI/CD 설계

### 1. CI: 슬래시 명령어 중심 테스트

#### Phase 1: 기본 검증 (모든 PR)
```yaml
name: CI - Basic Validation
on: [push, pull_request]

jobs:
  lint-and-format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Python Lint
        run: |
          pip install ruff black
          ruff check .
          black --check .
      
      - name: Shell Script Check
        run: |
          shellcheck *.sh
          
      - name: Markdown Lint
        uses: DavidAnson/markdownlint-cli2-action@v11
```

#### Phase 2: 슬래시 명령어 테스트
```yaml
  test-slash-commands:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        command: [기획, 구현, 안정화, 배포, 주간보고]
    steps:
      - name: Setup Test Environment
        run: |
          ./init.sh "test-${{ matrix.command }}" "CI Test"
          
      - name: Test Command Execution
        run: |
          # 명령어 파일 존재 확인
          test -f .claude/commands/${{ matrix.command }}.md
          
      - name: Validate Output Structure
        run: |
          python scripts/validate_command_output.py ${{ matrix.command }}
```

#### Phase 3: 프로젝트 템플릿 검증
```yaml
  test-project-templates:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        template: [basic, web, fullstack]
    steps:
      - name: Create Project with Template
        run: |
          ./init.sh "test-${{ matrix.template }}" "Template Test"
          
      - name: Verify Structure
        run: |
          # 필수 디렉토리 확인
          test -d src/test-${{ matrix.template }}/core
          test -d docs/CURRENT
          test -f CLAUDE.md
          
      - name: Run Template Tests
        run: |
          cd test-${{ matrix.template }}
          pytest tests/ --cov=src/
```

### 2. CD: 버전 릴리스 및 배포

#### 릴리스 워크플로우 (태그 기반)
```yaml
name: CD - Release
on:
  push:
    tags:
      - 'v*'

jobs:
  create-release:
    runs-on: ubuntu-latest
    steps:
      - name: Generate Release Notes
        run: |
          python scripts/generate_changelog.py > CHANGELOG.md
          
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            *.sh
            scripts/*
            .claude/commands/*
          generate_release_notes: true
          
      - name: Update Documentation
        run: |
          # 자동으로 버전 문서 업데이트
          python scripts/update_version_docs.py ${{ github.ref_name }}
```

#### 배포 알림 (Slack/Discord)
```yaml
      - name: Notify Release
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            🚀 Claude-dev-kit ${{ github.ref_name }} 릴리스
            📝 주요 변경사항: ${{ steps.changelog.outputs.summary }}
```

### 3. 회귀 테스트 전략

#### 일일 회귀 테스트 (Scheduled)
```yaml
name: Nightly Regression
on:
  schedule:
    - cron: '0 2 * * *'  # 매일 새벽 2시

jobs:
  regression-suite:
    runs-on: ubuntu-latest
    steps:
      - name: Full Command Suite Test
        run: |
          # 모든 명령어 조합 테스트
          ./scripts/run_regression_tests.sh --full
          
      - name: Performance Benchmark
        run: |
          # 성능 벤치마크
          python scripts/benchmark.py --compare-with-baseline
          
      - name: Compatibility Test
        run: |
          # 다양한 환경에서 호환성 테스트
          ./scripts/test_compatibility.sh
```

## 🎯 구현 우선순위 (수정)

### Week 1: 핵심 CI 구축
1. **기본 린팅/포매팅** ✅
2. **슬래시 명령어 검증** ✅
3. **PR 자동 체크** ✅

### Week 2: 테스트 확장
1. **템플릿 검증 자동화**
2. **통합 테스트 스위트**
3. **커버리지 리포팅**

### Week 3: CD 및 릴리스
1. **자동 버전 관리**
2. **릴리스 노트 생성**
3. **배포 알림 시스템**

## 📊 성공 지표 (조정)

| 지표 | 기존 목표 | 수정 목표 | 이유 |
|------|----------|----------|------|
| 테스트 커버리지 | 80% | 60% | 슬래시 명령어 특성상 |
| 빌드 시간 | 5분 | 3분 | 경량 테스트 |
| 회귀 테스트 주기 | 커밋마다 | 일일 | 리소스 효율화 |

## 🚀 즉시 실행 가능 액션

### Step 1: 최소 CI 설정 (오늘)
```bash
# .github/workflows/ci.yml 생성
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOF'
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: |
          ./init.sh "ci-test" "Automated Test"
          test -d .claude/commands
          test -f CLAUDE.md
EOF
```

### Step 2: 테스트 스크립트 작성
```python
# scripts/test_slash_commands.py
def test_command_files():
    """슬래시 명령어 파일 검증"""
    required_commands = [
        '기획', '구현', '안정화', '배포', 
        '주간보고', '문서정리', '레포정리'
    ]
    for cmd in required_commands:
        assert os.path.exists(f'.claude/commands/{cmd}.md')
```

### Step 3: 상태 배지 추가
```markdown
# README.md에 추가
[![CI Status](https://github.com/USER/claude-dev-kit/workflows/CI/badge.svg)](https://github.com/USER/claude-dev-kit/actions)
[![Coverage](https://codecov.io/gh/USER/claude-dev-kit/branch/main/graph/badge.svg)](https://codecov.io/gh/USER/claude-dev-kit)
```

## 💡 핵심 차별화 포인트

### Claude-dev-kit 특화 기능
1. **슬래시 명령어 검증**: 각 명령어 실행 시뮬레이션
2. **템플릿 무결성**: 생성된 프로젝트 구조 자동 검증
3. **문서 동기화**: CLAUDE.md 자동 업데이트 확인
4. **Git Hook 테스트**: pre-commit 훅 동작 검증

### 범용성 vs 특화
- **범용 적용 가능**: 린팅, 포매팅, 버전 관리
- **특화 필요**: 슬래시 명령어, 템플릿, Claude 통합
- **하이브리드 접근**: 기본 CI/CD + Claude-dev-kit 특화 레이어

## 📝 위험 관리

| 리스크 | 영향 | 대응 |
|--------|------|------|
| Claude API 의존성 | 높음 | Mock 테스트 환경 구축 |
| 로컬 환경 차이 | 중간 | Docker 컨테이너 활용 |
| 테스트 데이터 관리 | 낮음 | 최소 테스트 셋 유지 |

## ✅ 수정된 완료 조건

- [ ] 슬래시 명령어 자동 검증 ✅
- [ ] PR 체크 필수화 ✅
- [ ] 일일 회귀 테스트 ✅
- [ ] 자동 릴리스 프로세스 ✅
- [ ] 팀 가이드 문서 완성 ✅

---

*nf-core 사례를 참고하되, Claude-dev-kit의 특성에 맞게 조정된 CI/CD 전략*