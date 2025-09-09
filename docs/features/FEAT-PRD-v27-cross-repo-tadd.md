<!--
@meta
id: feature_20250905_1110_FEAT-PRD-v27-cross-repo-tadd
type: feature
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-05
tags: PRD, v27, FEAT-PRD-v27-cross-repo-tadd.md, FEAT, repo
related: 
-->

# PRD: Cross-Repository TADD Enforcement Package (v27.0)

## 1. 문제 정의

### 현재 상황
- **TADD Enforcement가 claude-dev-kit에만 존재**: 각 레포마다 수동 구현 필요
- **중복 작업**: 모든 프로젝트에서 동일한 설정을 반복
- **버전 불일치**: 레포마다 다른 버전의 TADD 규칙 적용
- **유지보수 어려움**: 개선사항을 모든 레포에 수동 반영

### 비즈니스 임팩트
- **생산성 저하**: 각 레포마다 30분+ 설정 시간 소요
- **일관성 부재**: 프로젝트별 품질 기준 상이
- **관리 복잡도**: 중앙 집중식 품질 관리 불가능

## 2. 목표

### 핵심 목표
**"One-Click TADD Enforcement: 어떤 레포든 1분 안에 TADD 적용"**

### 성공 지표
- 설치 시간 < 1분
- Zero Configuration 지원
- 자동 업데이트 메커니즘
- 언어/프레임워크 무관 적용

## 3. 솔루션: TADD-as-a-Package

### 3.1. 배포 전략 (3가지 옵션)

#### Option A: NPM Package (추천)
```bash
npx @claude-dev-kit/tadd-enforce init
# 또는
npm install -g @claude-dev-kit/tadd-enforce
tadd-enforce init
```

**장점**:
- NPM 생태계 활용 (대부분 개발자 익숙)
- 버전 관리 용이
- 자동 업데이트 가능

#### Option B: GitHub Template Repository
```bash
# GitHub UI에서 "Use this template" 클릭
# 또는
gh repo create my-project --template claude-dev-kit/tadd-template
```

**장점**:
- GitHub 네이티브 기능
- Fork와 달리 히스토리 없음
- Actions/Workflows 자동 포함

#### Option C: Curl Install Script
```bash
curl -sSL https://tadd.claude-dev-kit.io/install | bash
# 또는
wget -qO- https://tadd.claude-dev-kit.io/install | bash
```

**장점**:
- 의존성 없음
- 한 줄 설치
- CI/CD 파이프라인 통합 용이

### 3.2. 핵심 구성 요소

#### 1. Universal Installer (`tadd-enforce`)
```bash
#!/bin/bash
# 자동 감지 및 설정
detect_language()    # Python/JS/Go/Rust 등 자동 감지
detect_test_runner() # pytest/jest/go test 등 자동 감지
detect_ci_platform() # GitHub/GitLab/Bitbucket 자동 감지
install_hooks()      # Git hooks 자동 설치
setup_ci_workflow()  # CI 설정 자동 생성
```

#### 2. 언어별 어댑터
```yaml
adapters:
  python:
    test_command: pytest
    coverage_tool: pytest-cov
    mock_patterns: ["mock", "Mock", "patch"]
  
  javascript:
    test_command: npm test
    coverage_tool: jest --coverage
    mock_patterns: ["jest.mock", "sinon", "td.replace"]
  
  go:
    test_command: go test
    coverage_tool: go test -cover
    mock_patterns: ["gomock", "testify/mock"]
```

#### 3. CI/CD 템플릿
```yaml
# .github/workflows/tadd-enforce.yml (자동 생성)
name: TADD Enforcement
on: [push, pull_request]

jobs:
  tadd-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: claude-dev-kit/tadd-action@v1
        with:
          language: auto  # 자동 감지
          mock_limit: 20  # 커스터마이징 가능
          coverage_min: 80
```

### 3.3. 설치 프로세스

#### Step 1: 초기 설치
```bash
# 어떤 레포에서든 실행
npx @claude-dev-kit/tadd-enforce init

# 대화형 설정
? Project language: [Auto-detected: Python]
? Test framework: [Auto-detected: pytest]
? Mock usage limit: [20%]
? Coverage threshold: [80%]
? Install git hooks? [Y/n]
? Setup GitHub Actions? [Y/n]
```

#### Step 2: 자동 생성 파일
```
project/
├── .tadd/
│   ├── config.yml        # TADD 설정
│   └── version.lock      # 버전 고정
├── .github/
│   └── workflows/
│       └── tadd-enforce.yml  # CI/CD
├── .git/hooks/
│   ├── pre-push          # 로컬 검증
│   └── pre-commit        # 커밋 검증
└── scripts/
    ├── verify_tadd.sh    # 검증 스크립트
    └── quick_check.sh    # 빠른 체크
```

#### Step 3: 업데이트 메커니즘
```bash
# 자동 업데이트 체크 (매주)
tadd-enforce update

# 또는 CI에서 자동
- uses: claude-dev-kit/tadd-action@v1
  with:
    auto_update: true
```

### 3.4. 커스터마이징

#### `.tadd/config.yml`
```yaml
version: 1.0.0
language: python
rules:
  test_first: true
  mock_limit: 20
  coverage_min: 80
  
exceptions:
  - path: "legacy/*"
    reason: "Legacy code - gradual improvement"
  - path: "vendor/*"
    reason: "Third-party code"

notifications:
  slack: "https://hooks.slack.com/..."
  email: "team@example.com"
```

## 4. 구현 계획

### Phase 1: Core Package (1주)
- [ ] 언어 감지 로직
- [ ] Git hooks 생성기
- [ ] 기본 검증 스크립트

### Phase 2: CI/CD Integration (1주)
- [ ] GitHub Actions 템플릿
- [ ] GitLab CI 템플릿
- [ ] Jenkins 파이프라인

### Phase 3: Distribution (3일)
- [ ] NPM 패키지 배포
- [ ] GitHub Template 생성
- [ ] 설치 스크립트 호스팅

### Phase 4: Documentation (2일)
- [ ] README 작성
- [ ] 설치 가이드
- [ ] 트러블슈팅 문서

## 5. 마이그레이션 전략

### 기존 프로젝트
```bash
# 1. 백업
git checkout -b tadd-migration

# 2. 설치
npx @claude-dev-kit/tadd-enforce init --migrate

# 3. 점진적 적용
tadd-enforce init --gradual --days=30
```

### 신규 프로젝트
```bash
# Claude Dev Kit과 함께 설치
curl -sSL https://claude-dev-kit.io/install | bash
# TADD 자동 포함됨
```

## 6. 성공 메트릭

### 단기 (30일)
- 10개 이상 레포 적용
- 설치 성공률 > 95%
- 평균 설치 시간 < 60초

### 장기 (90일)
- 100개 이상 레포 적용
- 커뮤니티 기여 5건 이상
- 다국어 지원 (Python, JS, Go, Rust, Java)

## 7. 배포 채널

### Primary
- **NPM Registry**: 메인 배포 채널
- **GitHub Releases**: 바이너리 배포
- **Docker Hub**: 컨테이너화된 버전

### Secondary
- **Homebrew**: Mac 사용자
- **APT/YUM**: Linux 사용자
- **Chocolatey**: Windows 사용자

## 8. 예제: 실제 적용

### Python 프로젝트
```bash
cd my-python-project
npx @claude-dev-kit/tadd-enforce init
# ✅ Detected: Python 3.10, pytest
# ✅ Created: .github/workflows/tadd-enforce.yml
# ✅ Installed: Git hooks
# 🎉 TADD Enforcement ready!
```

### Node.js 프로젝트
```bash
cd my-node-project
npm install -D @claude-dev-kit/tadd-enforce
npm run tadd:init
# ✅ Detected: Node.js 18, Jest
# ✅ Updated: package.json scripts
# 🎉 TADD Enforcement ready!
```

### 언어 무관 (Docker)
```bash
docker run -v $(pwd):/app claude-dev-kit/tadd-enforce init
# ✅ Universal setup complete
# 🎉 TADD Enforcement ready!
```

## 9. 오픈소스 전략

### 라이선스
- MIT License (최대 호환성)

### 기여 가이드
- CONTRIBUTING.md 작성
- 언어별 어댑터 플러그인 시스템
- 커뮤니티 템플릿 갤러리

### 거버넌스
- Core Team: 핵심 기능
- Community: 언어 어댑터, 플러그인
- Advisory Board: 방향성 결정

---

**작성일**: 2025-09-02
**버전**: v27.0
**상태**: Planning → Ready for Implementation