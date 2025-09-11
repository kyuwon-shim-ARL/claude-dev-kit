# 🎭 Anti-Theater Testing Guide v2.0
**Theater Testing을 원천 차단하는 실전 가이드**

## 🔥 **핵심 원칙: "사용자가 실제로 할 수 있나?"**

**❌ Theater Testing**: "코드가 작동하나?"만 확인  
**✅ Real Testing**: "사용자가 실제로 이 기능을 쓸 수 있나?"를 확인

## 🚫 **절대 금지 패턴 (자동 거부 목록)**

### **Type 1: 존재 확인만 하는 테스트**
```python
# ❌ BANNED: 파일/객체 존재만 확인
def test_file_exists():
    assert os.path.exists('file.txt')  # 파일이 있기만 하면 통과

def test_result_not_none():
    result = function()
    assert result is not None  # None이 아니기만 하면 통과

# ✅ REQUIRED: 구체적 내용/기능 검증
def test_config_file_contains_valid_settings():
    """사용자가 설정 파일을 통해 실제로 시스템을 설정할 수 있는지"""
    config_path = 'config.yaml'
    
    # When: 설정 파일 로드
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Then: 필수 설정들이 유효한 값으로 있어야 함
    assert config['database']['host'] == 'localhost'
    assert config['database']['port'] == 5432
    assert config['api']['timeout'] > 0
    assert 'production' in config['environments']
```

### **Type 2: 자기 참조 테스트**
```python
# ❌ BANNED: 자기 자신과 비교
def test_function_returns_itself():
    result = get_data()
    assert result == result  # 의미없는 비교

# ❌ BANNED: 함수 호출만 확인
def test_function_runs():
    process_data()
    assert True  # 에러 없이 실행되기만 하면 통과

# ✅ REQUIRED: 실제 비즈니스 로직 검증
def test_user_data_processing_transforms_correctly():
    """사용자 데이터가 올바른 형태로 변환되는지"""
    # Given: 실제 사용자 입력 형태
    raw_user_data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'JOHN.DOE@EXAMPLE.COM',
        'age': '25'
    }
    
    # When: 처리 실행
    processed = process_user_data(raw_user_data)
    
    # Then: 구체적인 변환 결과 검증
    assert processed['full_name'] == 'John Doe'
    assert processed['email'] == 'john.doe@example.com'
    assert processed['age'] == 25  # 숫자 변환 확인
    assert processed['created_at'] is not None
```

### **Type 3: 단순 문자열/길이 확인**
```python
# ❌ BANNED: 단순 길이/포함 확인
def test_response_has_content():
    response = api_call()
    assert len(response) > 0  # 뭔가 있기만 하면 통과
    assert 'data' in response  # 키만 있으면 통과

# ✅ REQUIRED: 실제 데이터 구조와 값 검증
def test_user_profile_api_returns_complete_profile():
    """사용자가 프로필 API를 통해 완전한 프로필 정보를 받을 수 있는지"""
    # Given: 실제 사용자 ID
    user_id = 'user_123'
    
    # When: 프로필 API 호출
    response = get_user_profile(user_id)
    
    # Then: 실제 사용 가능한 프로필 데이터 검증
    assert response['user_id'] == 'user_123'
    assert response['username'].startswith('user_')
    assert '@' in response['email']  # 유효한 이메일 형태
    assert response['profile_picture_url'].startswith('https://')
    assert response['member_since'] <= datetime.now()
    assert response['status'] in ['active', 'inactive', 'suspended']
```

## ✅ **Real Testing 필수 패턴**

### **패턴 1: 실제 사용자 워크플로우 테스트**
```python
def test_complete_user_registration_workflow():
    """신규 사용자가 처음부터 끝까지 회원가입을 완료할 수 있는지"""
    
    # Step 1: 사용자가 회원가입 페이지 접속
    signup_page = navigate_to('/signup')
    assert signup_page.title == 'Sign Up - MyApp'
    
    # Step 2: 사용자가 정보 입력
    form_data = {
        'username': 'newuser123',
        'email': 'newuser@example.com', 
        'password': 'SecurePass123!',
        'confirm_password': 'SecurePass123!'
    }
    
    # Step 3: 폼 제출
    result = submit_signup_form(form_data)
    
    # Step 4: 성공 응답 확인
    assert result['status'] == 'success'
    assert result['user_id'] is not None
    assert result['verification_email_sent'] is True
    
    # Step 5: 실제 DB에 사용자 생성 확인
    created_user = get_user_by_email('newuser@example.com')
    assert created_user['username'] == 'newuser123'
    assert created_user['email_verified'] is False  # 아직 미인증
    assert created_user['status'] == 'pending_verification'
```

### **패턴 2: 에러 시나리오 테스트**
```python
def test_user_cannot_register_with_duplicate_email():
    """이미 존재하는 이메일로는 회원가입할 수 없는지"""
    
    # Given: 이미 존재하는 사용자
    existing_email = 'existing@example.com'
    create_user({'email': existing_email, 'username': 'existing_user'})
    
    # When: 같은 이메일로 회원가입 시도
    duplicate_signup = {
        'username': 'new_user',
        'email': existing_email,  # 중복 이메일
        'password': 'password123'
    }
    
    # Then: 구체적 에러 응답 확인
    with pytest.raises(ValidationError) as exc_info:
        submit_signup_form(duplicate_signup)
    
    assert 'already exists' in str(exc_info.value)
    assert exc_info.value.error_code == 'EMAIL_DUPLICATE'
    
    # And: 새로운 사용자가 생성되지 않았는지 확인
    users_with_email = get_users_by_email(existing_email)
    assert len(users_with_email) == 1  # 기존 1개만 존재
```

### **패턴 3: 통합 시나리오 테스트**
```python
def test_file_upload_and_processing_pipeline():
    """사용자가 파일을 업로드하고 처리 결과를 받을 수 있는지"""
    
    # Given: 실제 CSV 파일
    test_csv_content = """name,age,city
John Doe,25,New York
Jane Smith,30,Los Angeles"""
    
    test_file = create_temp_file('test_data.csv', test_csv_content)
    
    # When: 파일 업로드
    upload_response = upload_file(test_file)
    job_id = upload_response['job_id']
    
    # Then: 업로드 성공 확인
    assert upload_response['status'] == 'uploaded'
    assert upload_response['filename'] == 'test_data.csv'
    assert upload_response['file_size'] > 0
    
    # When: 처리 완료까지 대기
    wait_for_job_completion(job_id, timeout=30)
    
    # Then: 처리 결과 확인
    result = get_processing_result(job_id)
    assert result['status'] == 'completed'
    assert result['records_processed'] == 2
    assert result['output_data'][0]['name'] == 'John Doe'
    assert result['output_data'][0]['age'] == 25
    assert result['output_data'][1]['city'] == 'Los Angeles'
```

## 🧠 **Mental Models for Real Testing**

### **Model 1: "Can the user actually...?"**
모든 테스트 작성 전에 물어보세요:
- "사용자가 실제로 이 기능으로 원하는 결과를 얻을 수 있나?"
- "이 테스트가 실패하면 사용자가 실제로 무엇을 할 수 없게 되나?"

### **Model 2: "What would break the user experience?"**
- Happy Path: "사용자가 정상적으로 목표를 달성할 수 있나?"
- Error Path: "사용자가 실수해도 적절한 안내를 받을 수 있나?"
- Edge Path: "극단적 상황에서도 시스템이 안정적인가?"

### **Model 3: "End-to-End Value Chain"**
- Input: "사용자가 제공하는 실제 데이터 형태"
- Processing: "시스템이 실제로 수행하는 비즈니스 로직"
- Output: "사용자가 받는 실제 가치"

## 🎯 **실전 테스트 작성 체크리스트**

### ✅ **작성 전 확인사항**
- [ ] 이 테스트가 실패하면 실제 사용자가 무엇을 할 수 없게 되는가?
- [ ] 실제 사용자 데이터를 사용하고 있는가?
- [ ] 비즈니스 가치를 검증하고 있는가?
- [ ] 에러 상황도 포함하고 있는가?

### ✅ **Assertion 품질 확인**
- [ ] 구체적인 값/구조를 검증하는가? (not just existence)
- [ ] 사용자 관점에서 의미있는 검증인가?
- [ ] Mock이 20% 미만인가?
- [ ] 실제 데이터로 동작하는가?

### ✅ **시나리오 완성도 확인**
- [ ] Happy Path (정상 시나리오) 포함
- [ ] Error Path (오류 시나리오) 포함  
- [ ] Edge Path (경계값 시나리오) 포함
- [ ] Integration (통합 시나리오) 포함

## 🚀 **자동 Theater Testing 탐지 시스템**

다음 패턴이 감지되면 자동으로 거부:

```python
THEATER_PATTERNS = [
    r'assert.*is not None',
    r'assert.*exists\(\)',
    r'assert len\(.+\) > 0',
    r'assert .+ == .+\1',  # 자기 참조
    r'assert True',
    r'assert.*in.*result',  # 단순 포함 확인
    r'assert.*startswith',  # 단순 시작 문자 확인
]
```

## 💡 **결론: Real Testing의 핵심**

**Theater Testing**: "코드가 깨지지 않았나?"
**Real Testing**: "사용자가 실제로 가치를 얻을 수 있나?"

모든 테스트는 **사용자 시나리오**에서 시작해서 **비즈니스 가치 검증**으로 끝나야 합니다.