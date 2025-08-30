# PRD v24: 진정한 TADD 시스템적 강제 메커니즘

## 🎯 핵심 통찰
**"프롬프트는 권고, 시스템은 강제"** - TADD는 AI의 선의에 의존할 수 없고, 시스템적으로 강제되어야 한다.

## 📌 문제 정의

### 현재 TADD의 허점
```python
# 프롬프트: "테스트 먼저 작성해줘"
# AI 실제 행동:
def login(username, password):  # 1. 코드 먼저 작성
    return True

def test_login():  # 2. 테스트는 나중에
    assert login("user", "pass") == True  # 3. Mock으로 대충
```

### 진짜 문제
- **순서 강제 불가**: AI가 코드 먼저 작성해도 막을 수 없음
- **Mock 남발**: 실제 테스트가 아닌 가짜 테스트
- **검증 부재**: 테스트가 실제로 기능을 검증하는지 확인 불가

## 🏗️ 해결책: TADD Enforcement System

### 1. 테스트-코드 순서 강제 메커니즘

#### Git 커밋 히스토리 검증
```yaml
# .github/workflows/tadd-enforcement.yml
name: TADD Enforcement
on: pull_request

jobs:
  verify-test-first:
    runs-on: ubuntu-latest
    steps:
      - name: Check Test-First Development
        run: |
          # 커밋 히스토리에서 테스트와 구현 순서 확인
          python scripts/verify_tadd_order.py
```

#### 순서 검증 스크립트
```python
# scripts/verify_tadd_order.py
def verify_tadd_order():
    """테스트가 구현보다 먼저 작성되었는지 검증"""
    
    commits = get_pr_commits()
    
    for feature in extract_features(commits):
        test_commit = find_test_commit(feature)
        impl_commit = find_implementation_commit(feature)
        
        if not test_commit:
            fail(f"❌ {feature}: 테스트 없음")
        
        if impl_commit and impl_commit.timestamp < test_commit.timestamp:
            fail(f"❌ {feature}: 구현이 테스트보다 먼저 작성됨")
        
        # 테스트가 실패 상태로 커밋되었는지 확인
        if not was_test_failing_initially(test_commit):
            warn(f"⚠️ {feature}: 테스트가 처음부터 통과 (TDD 위반 가능성)")
    
    return True
```

### 2. Mock 사용률 자동 검사

#### Mock 검출 및 제한
```python
# scripts/detect_mock_usage.py
def analyze_mock_usage():
    """Mock 사용률을 분석하고 제한"""
    
    test_files = find_all_test_files()
    
    stats = {
        "total_tests": 0,
        "mock_tests": 0,
        "real_tests": 0
    }
    
    for test_file in test_files:
        ast_tree = parse_python_file(test_file)
        
        for test_method in find_test_methods(ast_tree):
            stats["total_tests"] += 1
            
            if uses_mock(test_method):
                stats["mock_tests"] += 1
                
                # Mock 사용 상세 분석
                mock_details = analyze_mock_details(test_method)
                
                if mock_details["mocks_external_service"]:
                    # 외부 서비스 Mock은 허용
                    pass
                elif mock_details["mocks_internal_logic"]:
                    # 내부 로직 Mock은 금지
                    fail(f"❌ Internal logic mocking detected: {test_method.name}")
            else:
                stats["real_tests"] += 1
    
    mock_percentage = (stats["mock_tests"] / stats["total_tests"]) * 100
    
    if mock_percentage > 20:
        fail(f"❌ Mock 사용률 {mock_percentage}% > 20% 제한")
    
    return stats
```

### 3. 실제 테스트 실행 강제

#### 테스트 커버리지 + 실행 검증
```yaml
# .github/workflows/test-execution.yml
jobs:
  enforce-real-tests:
    steps:
      - name: Run Tests with Coverage
        run: |
          # 테스트 실행 및 커버리지 측정
          pytest --cov=src --cov-report=json --tb=short
          
      - name: Verify Test Quality
        run: |
          python scripts/verify_test_quality.py coverage.json
```

#### 테스트 품질 검증
```python
# scripts/verify_test_quality.py
def verify_test_quality(coverage_file):
    """테스트가 실제로 코드를 실행하는지 검증"""
    
    coverage = load_coverage(coverage_file)
    
    # 1. 각 함수가 테스트에서 실제로 호출되는지 확인
    for module in coverage.modules:
        for function in module.functions:
            if function.is_public and not function.is_tested:
                fail(f"❌ {function.name} has no real test coverage")
            
            # 테스트가 다양한 경로를 커버하는지 확인
            if function.branch_coverage < 60:
                warn(f"⚠️ {function.name} branch coverage {function.branch_coverage}%")
    
    # 2. 테스트가 assertion을 포함하는지 확인
    for test_file in find_test_files():
        for test in parse_tests(test_file):
            if not has_assertions(test):
                fail(f"❌ {test.name} has no assertions")
            
            if assertion_count(test) < 2:
                warn(f"⚠️ {test.name} has only {assertion_count(test)} assertion")
    
    return True
```

### 4. PR 머지 게이트 설정

#### Branch Protection Rules
```yaml
# GitHub 설정 (자동 적용 스크립트)
branch_protection:
  main:
    required_status_checks:
      strict: true
      contexts:
        - "TADD Enforcement"
        - "Mock Usage Check"
        - "Test Quality Gate"
        - "Coverage >= 80%"
    
    enforce_admins: true
    dismiss_stale_reviews: true
    
    required_pull_request_reviews:
      dismiss_stale_reviews: true
      require_code_owner_reviews: true
```

#### 자동 PR 체크
```yaml
# .github/workflows/pr-gate.yml
name: PR Quality Gate
on: pull_request

jobs:
  tadd-gate:
    runs-on: ubuntu-latest
    steps:
      - name: TADD Compliance Check
        id: tadd
        run: |
          python scripts/check_tadd_compliance.py
          
      - name: Create Check Run
        uses: actions/github-script@v6
        with:
          script: |
            const status = ${{ steps.tadd.outputs.passed }} ? 'success' : 'failure';
            
            github.rest.checks.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              name: 'TADD Compliance',
              head_sha: context.sha,
              status: 'completed',
              conclusion: status,
              output: {
                title: 'TADD Enforcement Results',
                summary: ${{ steps.tadd.outputs.summary }}
              }
            });
```

### 5. Claude 프롬프트와 시스템 연동

#### /구현 명령어 개선
```python
# 새로운 /구현 워크플로우
def implement_with_tadd_enforcement(feature):
    """TADD를 시스템적으로 강제하는 구현 프로세스"""
    
    # Step 1: 테스트 먼저 생성 (실패하는 테스트)
    test_file = generate_failing_test(feature)
    commit(test_file, f"test: Add failing test for {feature}")
    
    # Step 2: CI에서 테스트 실패 확인
    run_ci_and_verify_failure()
    
    # Step 3: 최소 구현
    impl_file = generate_minimal_implementation(feature)
    commit(impl_file, f"feat: Implement {feature} (minimal)")
    
    # Step 4: CI에서 테스트 통과 확인
    run_ci_and_verify_success()
    
    # Step 5: 리팩토링
    refactored = refactor_implementation(impl_file)
    commit(refactored, f"refactor: Improve {feature} implementation")
    
    # Step 6: 추가 테스트
    additional_tests = generate_edge_case_tests(feature)
    commit(additional_tests, f"test: Add edge cases for {feature}")
    
    return {
        "test_first": True,
        "mock_usage": calculate_mock_percentage(),
        "coverage": get_coverage_report(),
        "ci_status": "passing"
    }
```

## 📊 실제 적용 예시

### 시나리오: 로그인 기능 구현

#### 1. 사용자 요청
```bash
/구현 "로그인 기능"
```

#### 2. Claude 실행 (시스템 강제)
```python
# Step 1: 실패하는 테스트 먼저 (자동 커밋)
# tests/test_login.py
def test_login_with_valid_credentials():
    result = login("user@example.com", "password123")  # 아직 구현 안됨
    assert result.success == True
    assert result.user.email == "user@example.com"

# Git commit: "test: Add failing test for login feature"
# CI 실행 → ❌ 테스트 실패 (예상된 결과)
```

#### 3. GitHub Actions 검증
```yaml
# CI 로그
✅ Test-first development verified
✅ Test is properly failing (not mocked)
⏳ Waiting for implementation...
```

#### 4. 구현 추가
```python
# Step 2: 최소 구현 (자동 커밋)
# src/auth/login.py
def login(email, password):
    # 실제 구현 (Mock 없음)
    user = db.query(User).filter_by(email=email).first()
    if user and user.check_password(password):
        return LoginResult(success=True, user=user)
    return LoginResult(success=False, user=None)

# Git commit: "feat: Implement login feature"
# CI 실행 → ✅ 테스트 통과
```

#### 5. 시스템 검증 결과
```yaml
TADD Compliance Report:
✅ Test committed before implementation
✅ Test was failing initially
✅ Mock usage: 0% (< 20% limit)
✅ Coverage: 85% (> 80% requirement)
✅ All assertions valid
✅ PR can be merged
```

## 🚀 즉시 구현 가능한 MVP

### Step 1: 기본 검증 스크립트
```bash
#!/bin/bash
# scripts/quick_tadd_check.sh

# 최근 커밋에서 테스트와 구현 순서 확인
TEST_COMMIT=$(git log --grep="^test:" -1 --format="%H")
FEAT_COMMIT=$(git log --grep="^feat:" -1 --format="%H")

if [ -z "$TEST_COMMIT" ]; then
    echo "❌ No test commit found"
    exit 1
fi

if git rev-list $FEAT_COMMIT..$TEST_COMMIT | grep -q .; then
    echo "✅ Test was committed before implementation"
else
    echo "❌ Implementation was committed before test"
    exit 1
fi
```

### Step 2: GitHub Actions 워크플로우
```yaml
# .github/workflows/tadd-mvp.yml
name: TADD MVP Check
on: [pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # 전체 히스토리 필요
          
      - name: Check TADD Order
        run: ./scripts/quick_tadd_check.sh
        
      - name: Check Mock Usage
        run: |
          MOCK_COUNT=$(grep -r "Mock\|mock\|@patch" tests/ | wc -l)
          TOTAL_TESTS=$(grep -r "def test_" tests/ | wc -l)
          
          if [ $MOCK_COUNT -gt $((TOTAL_TESTS / 5)) ]; then
            echo "❌ Too many mocks: $MOCK_COUNT/$TOTAL_TESTS"
            exit 1
          fi
```

## 💡 핵심 차별점

### 프롬프트 vs 시스템

| 항목 | 프롬프트만 | 시스템 강제 |
|------|----------|------------|
| 순서 강제 | ❌ 불가능 | ✅ Git 히스토리로 검증 |
| Mock 제한 | ❌ 권고만 | ✅ 자동 검사 및 차단 |
| 실행 검증 | ❌ 신뢰 기반 | ✅ CI에서 실제 실행 |
| 품질 보증 | ❌ 주관적 | ✅ 객관적 메트릭 |
| 회피 가능성 | ✅ 높음 | ❌ 불가능 |

## ✅ 성공 기준

- [ ] 모든 PR이 TADD 순서 검증 통과
- [ ] Mock 사용률 20% 이하 강제
- [ ] 테스트 커버리지 80% 이상 필수
- [ ] 실패→성공 사이클 추적 가능
- [ ] AI의 TADD 회피 0%

---

*이제 TADD는 선택이 아닌 필수가 됩니다. 시스템이 강제하기 때문입니다.*