# 테스트 엄밀성 레벨 가이드라인

## 🎯 엄밀성 레벨 정의

### Level 1: 기본 (Basic) - 70점
**최소 요구사항 - 모든 테스트는 이 수준 이상이어야 함**

```python
def test_user_can_login():
    """사용자가 올바른 계정으로 로그인할 수 있다"""
    # Given: 유효한 사용자 정보
    user_data = {"username": "john", "password": "secret123"}
    
    # When: 로그인 시도
    response = login_user(user_data)
    
    # Then: 성공 응답
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "token" in response.json()
```

**기준:**
- 구체적 값 검증 (200, True 등)
- 3개 이상 assertion
- Given-When-Then 구조

### Level 2: 견고 (Robust) - 85점  
**에러 케이스 + 경계값 포함**

```python
def test_user_login_with_error_cases():
    """사용자 로그인의 성공/실패 시나리오"""
    # Happy Path
    valid_response = login_user({"username": "john", "password": "secret123"})
    assert valid_response.status_code == 200
    assert valid_response.json()["user"]["id"] == 123
    
    # Error Cases
    with pytest.raises(AuthenticationError):
        login_user({"username": "john", "password": "wrong"})
    
    with pytest.raises(ValidationError):
        login_user({"username": "", "password": "secret123"})
    
    # Edge Cases  
    long_username = "a" * 255
    response = login_user({"username": long_username, "password": "secret"})
    assert response.status_code == 400
    assert "username too long" in response.json()["error"]
```

**추가 기준:**
- 최소 2개 에러 케이스
- 경계값 테스트 (빈 값, 최대값 등)
- 구체적 에러 메시지 검증

### Level 3: 포괄적 (Comprehensive) - 95점
**상태 변화 + 부작용 검증**

```python
def test_user_login_state_changes():
    """로그인 시 시스템 상태 변화 검증"""
    # Given: 초기 상태 확인
    user = User.get_by_username("john")
    assert user.last_login is None
    assert user.login_count == 0
    
    initial_session_count = Session.count()
    
    # When: 로그인 수행
    response = login_user({"username": "john", "password": "secret123"})
    
    # Then: 응답 검증
    assert response.status_code == 200
    token = response.json()["token"]
    assert jwt.decode(token)["user_id"] == user.id
    
    # And: 상태 변화 검증
    user.refresh_from_db()
    assert user.last_login is not None
    assert user.login_count == 1
    
    # And: 부작용 검증  
    assert Session.count() == initial_session_count + 1
    new_session = Session.get_by_token(token)
    assert new_session.user_id == user.id
    assert new_session.expires_at > timezone.now()
    
    # Cleanup
    new_session.delete()
```

**추가 기준:**
- 상태 변화 검증 (DB, 메모리 등)
- 부작용 검증 (세션, 로그 등)
- 시간 관련 검증
- 정리 과정 포함

### Level 4: 완벽 (Perfect) - 100점
**성능 + 동시성 + 보안 검증**

```python
def test_user_login_comprehensive():
    """로그인 기능의 완벽한 검증"""
    # Performance Test
    start_time = time.time()
    response = login_user({"username": "john", "password": "secret123"})
    execution_time = time.time() - start_time
    
    assert response.status_code == 200
    assert execution_time < 0.5  # 500ms 이하
    
    # Concurrency Test
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(login_user, {"username": f"user{i}", "password": "secret"})
            for i in range(10)
        ]
        results = [f.result() for f in futures]
        assert all(r.status_code == 200 for r in results)
    
    # Security Test
    # Rate limiting
    for _ in range(6):  # Assume 5 is the limit
        login_user({"username": "john", "password": "wrong"})
    
    response = login_user({"username": "john", "password": "wrong"})
    assert response.status_code == 429  # Too Many Requests
    
    # SQL Injection attempt
    malicious_input = {"username": "john'; DROP TABLE users;--", "password": "any"}
    response = login_user(malicious_input)
    assert response.status_code in [400, 401]  # Not 500 (server error)
    
    # JWT token validation
    valid_response = login_user({"username": "john", "password": "secret123"})
    token = valid_response.json()["token"]
    
    # Token should expire correctly
    with freeze_time("2025-01-01"):
        assert jwt.decode(token)["exp"] > time.time()
    
    with freeze_time("2025-12-31"):
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token)
```

**추가 기준:**
- 성능 검증 (응답시간, 메모리 사용)
- 동시성 테스트
- 보안 테스트 (인젝션, 레이트 리미팅)
- 시간 관련 엣지 케이스

## 📊 자동 레벨 판정 기준

### 점수 계산 공식

```python
def calculate_rigor_level(test_analysis):
    score = 0
    
    # 기본 점수 (70점)
    if test_analysis['has_specific_assertions']:
        score += 40
    if test_analysis['assertion_count'] >= 3:
        score += 20  
    if test_analysis['has_given_when_then']:
        score += 10
    
    # 견고함 점수 (15점)
    if test_analysis['error_cases'] >= 2:
        score += 10
    if test_analysis['has_edge_cases']:
        score += 5
    
    # 포괄성 점수 (10점)  
    if test_analysis['checks_state_changes']:
        score += 5
    if test_analysis['checks_side_effects']:
        score += 5
    
    # 완벽성 점수 (5점)
    if test_analysis['has_performance_checks']:
        score += 2
    if test_analysis['has_security_checks']:
        score += 2
    if test_analysis['has_concurrency_checks']:
        score += 1
    
    return min(score, 100)
```

## 🎯 기능별 요구 레벨

### 핵심 기능 (Level 3 필수)
- 인증/인가 시스템
- 결제 처리
- 데이터 저장/조회
- API 엔드포인트

### 일반 기능 (Level 2 필수)
- UI 컴포넌트  
- 유틸리티 함수
- 설정 관리
- 로깅

### 보조 기능 (Level 1 충분)
- 헬퍼 함수
- 상수 정의
- 간단한 변환 로직

## 🚨 레벨별 피드백 메시지

### Level 1 미달 (70점 미만)
```
❌ 테스트 품질 부족 (점수: 65)
개선 필요사항:
- 구체적 값 assertion 추가 (현재 1개, 최소 3개 필요)
- Given-When-Then 구조로 재작성
- Theater Testing 제거: "assert result is not None"
```

### Level 2 달성 제안 (70-84점)
```
⚠️ 테스트 견고성 개선 가능 (점수: 78)
개선 제안:
- 에러 케이스 2개 추가 (잘못된 입력, 권한 없음)
- 경계값 테스트 추가 (빈 값, 최대값)
- 예외 상황 검증 추가
```

### Level 3 달성 제안 (85-94점)
```
✅ 좋은 테스트! 완벽성을 위한 제안 (점수: 88)
고려사항:
- 상태 변화 검증 (DB 업데이트 확인)
- 부작용 검증 (로그, 이벤트 발생)
- 시간 관련 테스트 (타임스탬프, 만료)
```

이 가이드라인으로 **"어떤 테스트가 좋은 테스트인가?"**에 대한 명확한 기준을 제공합니다!