<!--
@meta
id: feature_20250905_1110_FEAT-PRD-v30.1-github-actions-deployment
type: feature
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-05
tags: PRD, v30.1, actions, github, FEAT
related: 
-->

# PRD: GitHub Actions 연동 진정한 배포 시스템 (v30.1)

## 1. 문제 정의

### 현재 상황 (심각한 문제)
```
/배포 실행 → git push → "배포 완료!" ✨
실제: GitHub Actions 3번 연속 실패 🔴
사용자: "왜 성공이라고 하는거야?" ← 완전히 정당한 지적
```

**핵심 문제:**
- **가짜 성공**: push만 되면 성공으로 처리
- **품질 게이트 무력화**: TADD enforcement 실패해도 모름
- **사용자 혼란**: 실제 상태와 다른 피드백
- **개발 효율성 저하**: 문제 발견이 늦어짐

## 2. 목표

### 핵심 목표: "Push ≠ Success"
**진정한 배포 성공 = Git Push + GitHub Actions All Pass**

### 성공 지표
- 가짜 성공 비율: 90% → 0%
- 실제 배포 성공률: 40% → 85%
- 문제 발견 시간: 나중에 → 즉시
- 사용자 만족도: 혼란 → 신뢰

## 3. 솔루션: 단순하고 직접적인 접근

### 3.1. GitHub CLI 기반 실시간 모니터링

**기본 원리:**
```bash
# GitHub CLI는 이미 완벽한 JSON 제공
gh run list --limit 1 --json status,conclusion,jobs,url
# 결과: 파싱하기 쉬운 구조화된 데이터

# Claude는 이미 세계 최고의 로그 분석 능력
# 복잡한 ML/패턴 DB 불필요 → 실시간 분석이 더 정확
```

### 3.2. 3단계 배포 프로세스

#### Phase A: Pre-Push 검증
```bash
echo "🔍 Pre-push TADD 검증..."
./scripts/quick_tadd_check.sh
if [ $? -ne 0 ]; then
    echo "❌ 로컬 검증 실패 - GitHub Actions도 실패할 예정"
    echo "먼저 로컬 문제를 해결하세요."
    exit 1
fi
```

#### Phase B: Push + 실시간 모니터링
```bash
echo "📤 원격 저장소로 푸시 중..."
git push origin main

echo "🔄 GitHub Actions 실시간 모니터링 시작..."
wait_for_github_actions  # 새로 구현할 함수
```

#### Phase C: 성공/실패 처리
```bash
wait_for_github_actions() {
    for i in {1..20}; do  # 5분 대기 (15초 간격)
        local status=$(gh run list --limit 1 --json status,conclusion --jq '.[0] | "\(.status):\(.conclusion)"')
        
        case $status in
            "completed:success")
                echo "✅ GitHub Actions: 전체 통과!"
                echo "🎉 진정한 배포 완료!"
                return 0
                ;;
            "completed:failure"|"completed:cancelled")
                echo "❌ GitHub Actions: 실패 ($status)"
                analyze_and_suggest_fix  # Claude 분석 요청
                return 1
                ;;
            "in_progress:"|"queued:")
                echo "⏳ 진행중... ($i/20) - $(date '+%H:%M:%S')"
                sleep 15
                ;;
        esac
    done
    
    echo "⏰ 타임아웃 (5분) - 수동 확인 필요"
    local run_url=$(gh run list --limit 1 --json url --jq '.[0].url')
    echo "🔗 GitHub에서 직접 확인: $run_url"
    return 1
}
```

### 3.3. 실패 분석 및 해결방안 (Claude 활용)

```bash
analyze_and_suggest_fix() {
    echo ""
    echo "🔍 실패 원인 분석 중..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # GitHub Actions 실패 로그 가져오기
    local failure_log=$(gh run view --log-failed 2>&1)
    
    echo "📋 실패 로그:"
    echo "$failure_log"
    echo ""
    
    # 기본 패턴 매칭 (간단하고 효과적)
    if echo "$failure_log" | grep -q "ImportError\|ModuleNotFoundError"; then
        suggest_import_fix
    elif echo "$failure_log" | grep -q "coverage.*fail\|Coverage failure"; then
        suggest_coverage_fix
    elif echo "$failure_log" | grep -q "test.*failed\|pytest.*FAILED"; then
        suggest_test_fix
    else
        suggest_general_fix
    fi
    
    echo ""
    echo "💡 다음 단계:"
    echo "1. 위 제안사항 적용"
    echo "2. 로컬에서 테스트: ./scripts/quick_tadd_check.sh"
    echo "3. 다시 배포: /배포"
}

suggest_import_fix() {
    echo "🔧 자동 감지: Python Import 오류"
    echo ""
    echo "💊 해결방안:"
    echo "• 누락된 파일 확인: ls -la scripts/ tests/"
    echo "• __init__.py 파일 추가"
    echo "• PYTHONPATH 설정: export PYTHONPATH=\$PWD"
    echo "• 로컬 테스트: python -c 'import sys; print(sys.path)'"
}

suggest_coverage_fix() {
    echo "🔧 자동 감지: 테스트 커버리지 부족"
    echo ""
    echo "💊 해결방안:"
    echo "• 현재 커버리지 확인: pytest --cov=scripts --cov-report=term"
    echo "• 테스트 파일 추가 필요"
    echo "• 또는 임계값 조정: .github/workflows/tadd-enforcement.yml에서 --cov-fail-under 값 조정"
}
```

## 4. 구현 계획

### Phase 1: 핵심 모니터링 (30분)
**목표**: `/배포` 명령어에 GitHub Actions 실시간 모니터링 추가

**구현 항목:**
- [ ] `wait_for_github_actions()` 함수 작성
- [ ] `.claude/commands/배포.md` 파일 수정
- [ ] 성공/실패/진행중 3가지 상태 처리
- [ ] 실패 시 `gh run view --log-failed` 출력

**성공 기준:**
- [x] push 후 자동으로 GitHub Actions 상태 추적
- [x] 실패 시 "가짜 성공" 메시지 없음
- [x] 실제 성공 시에만 "배포 완료" 메시지

### Phase 2: 슬래시 명령어 완전 통합 (1시간)
**목표**: 모든 관련 슬래시 명령어에 GitHub Actions 인식 통합

**구현 항목:**
- [ ] `/배포.md` 전체 개편
- [ ] `/안정화.md`에 pre-push 검증 추가
- [ ] `scripts/monitor_github_actions.sh` 독립 스크립트
- [ ] `analyze_and_suggest_fix()` 함수 구현

**성공 기준:**
- [x] 모든 배포 관련 명령어가 GitHub Actions 인식
- [x] 실패 시 구체적 해결방안 제시
- [x] 재시도 루프 제공

## 5. 기술 스펙

### 5.1. 의존성
- **필수**: `gh` (GitHub CLI) - 이미 설치됨
- **필수**: `jq` - JSON 파싱용
- **선택**: `curl` - 백업 API 호출용

### 5.2. 핵심 함수들

```bash
# GitHub Actions 상태 확인 (단순)
check_github_status() {
    gh run list --limit 1 --json status,conclusion --jq '.[0] | "\(.status):\(.conclusion)"'
}

# 실시간 모니터링 (핵심)
wait_for_github_actions() {
    # 위에서 정의한 로직
}

# 실패 분석 (Claude 활용)
analyze_and_suggest_fix() {
    # 위에서 정의한 로직
}
```

### 5.3. 에러 처리
```bash
# GitHub CLI 없는 경우
if ! command -v gh >/dev/null 2>&1; then
    echo "⚠️ GitHub CLI (gh) 필요 - 설치 후 다시 시도"
    echo "설치: https://cli.github.com/"
    exit 1
fi

# GitHub 인증 없는 경우
if ! gh auth status >/dev/null 2>&1; then
    echo "⚠️ GitHub 인증 필요 - gh auth login 실행"
    exit 1
fi

# 네트워크 오류 처리
if ! gh run list >/dev/null 2>&1; then
    echo "⚠️ GitHub API 접근 실패 - 네트워크 확인"
    echo "수동 확인: https://github.com/$(gh repo view --json owner,name --jq '.owner.login + \"/\" + .name')/actions"
    exit 1
fi
```

## 6. 성공 기준

### 정량적 목표
- **가짜 성공 제거**: 100% → 0%
- **실제 배포 성공률**: 40% → 85%
- **평균 문제 해결 시간**: 무한대 → 15분
- **사용자 재시도 횟수**: 3-5회 → 1-2회

### 정성적 목표
- **사용자 피드백**: "왜 성공이라고 해?" → "GitHub Actions도 통과했네!"
- **Claude 응답**: "배포 완료!" → "TADD enforcement 포함 진정한 배포 완료!"
- **개발 경험**: 혼란 → 신뢰

## 7. 위험 요소 및 대응

### Risk 1: GitHub API 한도
**대응**: 15초 간격으로 체크 (시간당 240회 << API 한도 5000회)

### Risk 2: 네트워크 불안정
**대응**: 실패 시 수동 확인 URL 제공 + 재시도 옵션

### Risk 3: 사용자 습관 변화 저항
**대응**: 기존 `/배포` 명령어 유지, 기능만 강화

## 8. 마이그레이션 가이드

### 기존 사용자
**변화 없음**: 계속 `/배포` 사용
**개선점**: 이제 진짜 성공할 때까지 기다림

### 새로운 기능
- GitHub Actions 실시간 상태 확인
- 실패 시 자동 분석 및 해결방안
- 재시도 루프 지원

---

**작성일**: 2025-09-02
**버전**: v30.1
**상태**: Ready for Implementation
**예상 완료**: 1.5시간