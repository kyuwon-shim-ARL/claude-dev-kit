#!/bin/bash
#
# GitHub Actions 실시간 모니터링 스크립트
# PRD v30.1 - 단순하고 직접적인 접근
#

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🔄 GitHub Actions 실시간 모니터링"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 필수 도구 확인
check_requirements() {
    if ! command -v gh >/dev/null 2>&1; then
        echo -e "${RED}❌ GitHub CLI (gh) 필요${NC}"
        echo "설치: https://cli.github.com/"
        exit 1
    fi

    if ! gh auth status >/dev/null 2>&1; then
        echo -e "${RED}❌ GitHub 인증 필요${NC}"
        echo "실행: gh auth login"
        exit 1
    fi

    if ! gh run list >/dev/null 2>&1; then
        echo -e "${RED}❌ GitHub API 접근 실패${NC}"
        echo "네트워크 상태 확인 또는 저장소 권한 확인"
        exit 1
    fi
}

# GitHub Actions 상태 확인 (단순)
check_github_status() {
    local status_info
    status_info=$(gh run list --limit 1 --json status,conclusion,url 2>/dev/null)
    
    if [ -z "$status_info" ] || [ "$status_info" = "[]" ]; then
        echo "no_runs"
        return
    fi
    
    local status conclusion url
    status=$(echo "$status_info" | jq -r '.[0].status // "unknown"')
    conclusion=$(echo "$status_info" | jq -r '.[0].conclusion // "null"')
    url=$(echo "$status_info" | jq -r '.[0].url // ""')
    
    echo "$status:$conclusion:$url"
}

# 실시간 모니터링 (핵심 함수)
wait_for_github_actions() {
    echo "📊 최신 GitHub Actions 상태 확인 중..."
    
    local run_info
    run_info=$(check_github_status)
    
    if [ "$run_info" = "no_runs" ]; then
        echo -e "${YELLOW}⚠️ GitHub Actions 실행 기록이 없습니다${NC}"
        echo "Push가 제대로 되었는지 확인하세요."
        return 1
    fi
    
    IFS=':' read -r status conclusion url <<< "$run_info"
    
    echo -e "${BLUE}🔗 실시간 상태: $url${NC}"
    echo ""
    
    # 이미 완료된 경우 즉시 결과 반환
    if [ "$status" = "completed" ]; then
        if [ "$conclusion" = "success" ]; then
            echo -e "${GREEN}✅ GitHub Actions: 전체 통과!${NC}"
            echo -e "${GREEN}🎉 진정한 배포 완료!${NC}"
            return 0
        else
            echo -e "${RED}❌ GitHub Actions: 실패 ($conclusion)${NC}"
            return 1
        fi
    fi
    
    # 진행중인 경우 실시간 모니터링
    echo "⏳ GitHub Actions 진행중... 실시간 모니터링 시작"
    echo ""
    
    for i in {1..20}; do  # 5분 대기 (15초 간격)
        run_info=$(check_github_status)
        IFS=':' read -r status conclusion url <<< "$run_info"
        
        case "$status" in
            "completed")
                echo ""
                if [ "$conclusion" = "success" ]; then
                    echo -e "${GREEN}✅ GitHub Actions: 전체 통과!${NC}"
                    echo -e "${GREEN}🎉 진정한 배포 완료!${NC}"
                    return 0
                else
                    echo -e "${RED}❌ GitHub Actions: 실패 ($conclusion)${NC}"
                    return 1
                fi
                ;;
            "in_progress"|"queued")
                local timestamp=$(date '+%H:%M:%S')
                echo -ne "\\r⏳ 진행중... [$i/20] $timestamp - 상태: $status"
                sleep 15
                ;;
            *)
                echo -ne "\\r🔍 상태 확인중... [$i/20] $(date '+%H:%M:%S')"
                sleep 15
                ;;
        esac
    done
    
    echo ""
    echo -e "${YELLOW}⏰ 타임아웃 (5분 초과)${NC}"
    echo -e "${BLUE}🔗 수동 확인: $url${NC}"
    return 1
}

# 실패 분석 및 해결방안 (Claude 활용)
analyze_and_suggest_fix() {
    echo ""
    echo "🔍 실패 원인 분석 중..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # GitHub Actions 실패 로그 가져오기
    echo "📋 실패 로그 가져오는 중..."
    local failure_log
    failure_log=$(gh run view --log-failed 2>&1)
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 실패 로그를 가져올 수 없습니다${NC}"
        echo "수동으로 확인하세요: $(gh run list --limit 1 --json url --jq '.[0].url')"
        return 1
    fi
    
    echo "📋 실패 로그:"
    echo "$failure_log"
    echo ""
    
    # 기본 패턴 매칭 (간단하고 효과적)
    if echo "$failure_log" | grep -q "ImportError\\|ModuleNotFoundError"; then
        suggest_import_fix
    elif echo "$failure_log" | grep -q "coverage.*fail\\|Coverage failure"; then
        suggest_coverage_fix
    elif echo "$failure_log" | grep -q "test.*failed\\|pytest.*FAILED"; then
        suggest_test_fix
    else
        suggest_general_fix
    fi
    
    echo ""
    echo -e "${BLUE}💡 다음 단계:${NC}"
    echo "1. 위 제안사항 적용"
    echo "2. 로컬에서 테스트: ./scripts/quick_tadd_check.sh"
    echo "3. 다시 배포: /배포"
    echo ""
    echo -e "${YELLOW}또는 Claude에게 위 로그를 보여주고 분석을 요청하세요${NC}"
}

suggest_import_fix() {
    echo -e "${YELLOW}🔧 자동 감지: Python Import 오류${NC}"
    echo ""
    echo -e "${GREEN}💊 해결방안:${NC}"
    echo "• 누락된 파일 확인: ls -la scripts/ tests/"
    echo "• __init__.py 파일 추가가 필요할 수 있음"
    echo "• PYTHONPATH 설정: export PYTHONPATH=\$PWD"
    echo "• 로컬 테스트: python -c 'import sys; print(sys.path)'"
}

suggest_coverage_fix() {
    echo -e "${YELLOW}🔧 자동 감지: 테스트 커버리지 부족${NC}"
    echo ""
    echo -e "${GREEN}💊 해결방안:${NC}"
    echo "• 현재 커버리지 확인: pytest --cov=scripts --cov-report=term"
    echo "• 테스트 파일 추가 필요"
    echo "• 또는 임계값 조정: .github/workflows/tadd-enforcement.yml에서 --cov-fail-under 값 조정"
}

suggest_test_fix() {
    echo -e "${YELLOW}🔧 자동 감지: 테스트 실행 실패${NC}"
    echo ""
    echo -e "${GREEN}💊 해결방안:${NC}"
    echo "• 로컬에서 테스트 실행: python -m pytest tests/ -v"
    echo "• 실패하는 특정 테스트 확인"
    echo "• 테스트 파일의 import 경로 확인"
    echo "• 테스트 데이터나 fixture 누락 확인"
}

suggest_general_fix() {
    echo -e "${YELLOW}🔧 일반적인 GitHub Actions 실패${NC}"
    echo ""
    echo -e "${GREEN}💊 해결방안:${NC}"
    echo "• GitHub Actions 워크플로우 파일 확인: .github/workflows/"
    echo "• 환경 변수나 시크릿 설정 확인"
    echo "• 의존성 설치 실패 여부 확인"
    echo "• 로컬과 CI 환경의 차이점 분석"
}

# 메인 실행 함수
main() {
    check_requirements
    
    if wait_for_github_actions; then
        echo ""
        echo -e "${GREEN}🎉 배포 성공! 모든 검증을 통과했습니다.${NC}"
        exit 0
    else
        analyze_and_suggest_fix
        echo ""
        echo -e "${RED}❌ 배포 실패 - 문제를 해결한 후 다시 시도하세요.${NC}"
        exit 1
    fi
}

# 스크립트가 직접 실행된 경우
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi