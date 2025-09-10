# /연구 통합 명령어 사용자 시나리오 테스트 계획

## 📋 테스트 개요
- **목적**: 실제 사용자 워크플로우에서 /연구 명령어 완전성 검증
- **범위**: 신규 사용자부터 파워 유저까지 모든 시나리오
- **기준**: 실제 연구자의 일일 워크플로우 재현

## 🎯 핵심 사용자 시나리오

### 시나리오 1: 신규 연구 프로젝트 시작 (초보 사용자)
```bash
# Step 1: 프로젝트 생성 (정식 명령어)
/연구 init drug_discovery "신약 개발 연구 프로젝트"

# 예상 결과:
# - research_projects/2025-09-10_drug_discovery/ 생성
# - README.md, timeline.md 자동 생성
# - 하위 폴더 구조 완성 (notebooks/, data/, results/, etc.)

# Step 2: 첫 진행사항 기록
/연구 track "프로젝트 설정 완료, ChEMBL 데이터베이스 조사 시작"

# Step 3: 프로젝트 상태 확인
/연구 status

# 검증 포인트:
# - 폴더 구조가 완전히 생성되었는가?
# - timeline.md에 정확한 타임스탬프와 함께 기록되었는가?
# - status가 올바른 통계를 보여주는가?
```

### 시나리오 2: 파워 유저 워크플로우 (별칭 활용)
```bash
# Step 1: 빠른 프로젝트 생성 (1글자 별칭)
/연구 i protein_analysis "단백질 구조 분석"

# Step 2: 연속적인 진행 기록 (한글)
/연구 진행 "PDB 데이터 다운로드 완료"
/연구 t "AlphaFold 구조 분석 시작"
/연구 기록 "첫 번째 모델링 결과 확인"

# Step 3: 실험 시작 (영어 단축)
/연구 exp baseline_docking "기본 도킹 시뮬레이션"

# Step 4: 가설 설정
/연구 h "새로운 결합 부위가 더 높은 친화력을 보일 것"

# Step 5: 연속 명령 (체이닝)
/연구 m "Phase1" "기본 구조 분석 완료" && /연구 c "첫날 작업 마무리"

# 검증 포인트:
# - 모든 별칭이 정확히 인식되는가?
# - 한글 명령어가 올바르게 처리되는가?
# - 연속 명령 실행이 문제없는가?
```

### 시나리오 3: 기존 프로젝트 계속 작업
```bash
# 기존 SMILES 프로젝트에서 작업 재개
# (research_projects/2025-09-10_smiles_rgcca_chemical_space 존재)

# Step 1: 현재 상태 확인
/연구 s

# Step 2: 새로운 실험 추가
/연구 e attention_v2 "Attention mechanism 개선 버전"

# Step 3: 검색 기능 테스트
/연구 f "RGCCA"

# Step 4: 백업 생성
/연구 b

# 검증 포인트:
# - 기존 프로젝트 데이터가 올바르게 표시되는가?
# - 새 실험이 기존 구조에 잘 추가되는가?
# - 검색이 정확한 결과를 반환하는가?
```

### 시나리오 4: 에러 시나리오 처리
```bash
# Step 1: 잘못된 서브커맨드
/연구 wrong_command "test"
# 예상: 도움말 메시지 표시

# Step 2: 프로젝트 없는 상태에서 track
rm -rf research_projects/  # 테스트용 삭제
/연구 track "test message"
# 예상: "프로젝트가 없습니다" 메시지

# Step 3: 빈 인자로 init
/연구 init
# 예상: 적절한 에러 메시지

# Step 4: 권한 없는 디렉토리
cd /root  # 권한 없는 곳으로 이동
/연구 init test_project "test"
# 예상: 권한 에러 처리

# 검증 포인트:
# - 에러 메시지가 명확하고 도움이 되는가?
# - 시스템이 안정적으로 처리하는가?
# - 복구 방법이 제시되는가?
```

## 🧪 자동화된 테스트 스크립트

### test_research_command.sh
```bash
#!/bin/bash

# 테스트 환경 설정
TEST_DIR="/tmp/research_command_test"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Claude dev-kit 경로 설정
CLAUDE_DIR="/home/kyuwon/projects/claude-dev-kit"
RESEARCH_CMD="bash ${CLAUDE_DIR}/.claude/commands/연구.md"

# 테스트 카운터
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 테스트 함수
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_pattern="$3"
    
    echo "🧪 Testing: $test_name"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    # 명령 실행
    output=$(eval "$command" 2>&1)
    exit_code=$?
    
    # 결과 확인
    if [[ "$output" =~ $expected_pattern ]] && [ $exit_code -eq 0 ]; then
        echo "✅ PASS: $test_name"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo "❌ FAIL: $test_name"
        echo "   Expected pattern: $expected_pattern"
        echo "   Actual output: $output"
        echo "   Exit code: $exit_code"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    echo ""
}

# 테스트 실행
echo "🚀 Starting Research Command Integration Tests"
echo "=============================================="

# 1. 기본 기능 테스트
run_test "Project Creation" \
    "$RESEARCH_CMD init test_project 'Test Project Description'" \
    "✅ 프로젝트 생성.*test_project"

run_test "Track Progress" \
    "$RESEARCH_CMD track 'First progress note'" \
    "✅ 진행사항 기록.*First progress note"

run_test "Status Check" \
    "$RESEARCH_CMD status" \
    "📊 연구 프로젝트 현황"

# 2. 별칭 테스트
run_test "1-letter Alias (i for init)" \
    "$RESEARCH_CMD i alias_test 'Alias Test'" \
    "✅ 프로젝트 생성.*alias_test"

run_test "Korean Alias (상태 for status)" \
    "$RESEARCH_CMD 상태" \
    "📊 연구 프로젝트 현황"

run_test "English Shortcut (exp for experiment)" \
    "$RESEARCH_CMD exp test_exp 'Test Experiment'" \
    "✅ 실험 시작"

# 3. 에러 처리 테스트
run_test "Invalid Subcommand" \
    "$RESEARCH_CMD invalid_cmd" \
    "❌ 알 수 없는 서브커맨드"

run_test "Empty Project Name" \
    "$RESEARCH_CMD init" \
    "(에러 메시지 패턴)"

# 최종 결과
echo "📊 Test Results Summary"
echo "======================"
echo "Total Tests: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS"
echo "Failed: $FAILED_TESTS"
echo "Success Rate: $(( PASSED_TESTS * 100 / TOTAL_TESTS ))%"

# 정리
cd /
rm -rf "$TEST_DIR"

if [ $FAILED_TESTS -eq 0 ]; then
    echo "🎉 All tests passed!"
    exit 0
else
    echo "❌ Some tests failed!"
    exit 1
fi
```

## 📊 성능 및 사용성 메트릭

### 응답 시간 측정
```bash
# 각 명령어별 실행 시간 측정
time /연구 init speed_test "Speed Test"
time /연구 track "Performance test message"
time /연구 status
time /연구 list
```

### 메모리 사용량 측정
```bash
# 메모리 사용량 모니터링
/usr/bin/time -v /연구 init memory_test "Memory Test" 2>&1 | grep "Maximum resident set size"
```

### 사용성 지표
- 명령어 길이: 평균 글자 수
- 에러율: 잘못된 사용 시 에러 비율
- 학습 시간: 새 사용자가 익히는 시간

## 🎯 합격 기준

### 기능 요구사항
- ✅ 모든 서브커맨드 100% 작동
- ✅ 모든 별칭 정확히 인식 (100%)
- ✅ 에러 처리 적절한 메시지 (100%)
- ✅ 기존 데이터 무결성 (100%)

### 성능 요구사항
- ⏱️ 명령 실행 시간: <2초
- 💾 메모리 사용량: <10MB
- 📁 파일 생성: 100% 성공률

### 사용성 요구사항
- 📝 도움말 메시지: 명확하고 실용적
- 🔤 별칭 일관성: 직관적이고 기억하기 쉬움
- 🚫 에러 복구: 명확한 해결 방법 제시

## 🔄 다음 단계: 테스트 실행

1. **자동화된 테스트 실행**
2. **수동 시나리오 검증**
3. **성능 측정**
4. **문제점 발견 시 구현 단계로 이동**
5. **모든 테스트 통과 시 검증 단계로 진행**