# /연구-통합 - 지능형 연구 관리 시스템

## 사용법
```
/연구-통합 [서브커맨드] [인자]
```

## 자동 모드 선택
Python이 있으면 고급 기능, 없으면 Bash 모드로 자동 전환

## 실행 프로토콜

```bash
#!/bin/bash

# Python 가용성 체크
if python3 -c "import sys; sys.path.append('/home/kyuwon/projects/claude-dev-kit/src'); from research_manager_hybrid import HybridResearchManager" 2>/dev/null; then
    echo "🐍 Python 모드로 실행"
    python3 -c "
import sys
sys.path.append('/home/kyuwon/projects/claude-dev-kit/src')
from research_manager_hybrid import HybridResearchManager

m = HybridResearchManager()

# 서브커맨드 처리
subcommand = '$1'
args = '$2'

if subcommand in ['init', '시작', '초기화']:
    m.init_project(args, '$3')
elif subcommand in ['track', '진행', '기록']:
    m.track_progress(args)
elif subcommand in ['experiment', '실험']:
    m.start_experiment(args, '$3')
elif subcommand in ['hypothesis', '가설']:
    m.set_hypothesis(args)
elif subcommand in ['milestone', '마일스톤']:
    m.set_milestone(args, '$3')
elif subcommand in ['status', '상태']:
    m.show_status()
elif subcommand in ['list', '목록']:
    m.list_projects()
else:
    print(f'Unknown command: {subcommand}')
"
else
    echo "📁 Bash 모드로 실행"
    
    # Bash 구현
    case "$1" in
        init|시작|초기화)
            PROJECT_NAME="$2"
            PROJECT_DIR="research_projects/$(date +%Y-%m-%d)_${PROJECT_NAME}"
            mkdir -p "${PROJECT_DIR}"/{notebooks,data,results,figures,docs,scripts,experiments}
            
            cat > "${PROJECT_DIR}/README.md" << EOF
# ${PROJECT_NAME}
Created: $(date '+%Y-%m-%d %H:%M')
Description: $3
EOF
            
            cat > "${PROJECT_DIR}/timeline.md" << EOF
# Research Timeline - ${PROJECT_NAME}
## Project Start: $(date '+%Y-%m-%d %H:%M')
---
EOF
            
            echo "✅ 프로젝트 생성: ${PROJECT_DIR}"
            ;;
            
        track|진행|기록)
            ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
            if [ -z "$ACTIVE_PROJECT" ]; then
                echo "❌ 활성 프로젝트가 없습니다"
                exit 1
            fi
            
            cat >> "${ACTIVE_PROJECT}/timeline.md" << EOF

## $(date '+%Y-%m-%d %H:%M')
$2
EOF
            
            echo "✅ 진행사항 기록: $2"
            ;;
            
        experiment|실험)
            ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
            EXP_NAME="$2"
            EXP_DIR="${ACTIVE_PROJECT}/experiments/$(date +%Y%m%d_%H%M)_${EXP_NAME}"
            
            mkdir -p "${EXP_DIR}"
            cat > "${EXP_DIR}/README.md" << EOF
# Experiment: ${EXP_NAME}
- Started: $(date '+%Y-%m-%d %H:%M')
- Description: $3
- Status: Running
EOF
            
            echo "✅ 실험 시작: ${EXP_DIR}"
            ;;
            
        status|상태)
            echo "📊 연구 프로젝트 현황"
            echo "===================="
            
            for PROJECT_DIR in research_projects/*/; do
                if [ -d "$PROJECT_DIR" ]; then
                    PROJECT_NAME=$(basename "$PROJECT_DIR")
                    TIMELINE_ENTRIES=$(grep -c "^##" "${PROJECT_DIR}/timeline.md" 2>/dev/null || echo 0)
                    EXP_COUNT=$(ls -d "${PROJECT_DIR}"/experiments/* 2>/dev/null | wc -l)
                    
                    echo ""
                    echo "📁 ${PROJECT_NAME}"
                    echo "   진행: ${TIMELINE_ENTRIES} 항목"
                    echo "   실험: ${EXP_COUNT}개"
                    
                    LAST_ENTRY=$(grep "^##" "${PROJECT_DIR}/timeline.md" 2>/dev/null | tail -1)
                    if [ -n "$LAST_ENTRY" ]; then
                        echo "   최근: ${LAST_ENTRY#\#\# }"
                    fi
                fi
            done
            ;;
            
        *)
            echo "❌ 알 수 없는 명령: $1"
            echo "사용 가능한 명령: init, track, experiment, hypothesis, milestone, status, list"
            ;;
    esac
fi
```

## 지원 명령어

### 핵심 명령어 (Bash/Python 모두 지원)
- `init [이름] [설명]` - 프로젝트 생성
- `track [내용]` - 진행사항 기록
- `experiment [이름] [설명]` - 실험 시작
- `hypothesis [가설]` - 가설 설정
- `milestone [이름] [설명]` - 마일스톤
- `checkpoint [메모]` - 체크포인트
- `status` - 현황 확인
- `list` - 프로젝트 목록

### 고급 명령어 (Python 모드만)
- `analyze` - 데이터 분석
- `visualize` - 시각화 생성
- `report` - 보고서 생성
- `ml-track` - ML 실험 추적
- `api-sync` - 외부 API 동기화

## 장점

1. **자동 전환**: 환경에 따라 최적 모드 선택
2. **하위 호환**: 기존 명령 모두 지원
3. **점진적 업그레이드**: Python 설치 시 자동으로 고급 기능 활성화
4. **단일 진입점**: 사용자는 하나의 명령어만 기억

## 마이그레이션 가이드

```bash
# 기존 명령어 → 새 명령어
/연구 → /연구-통합
/research → /연구-통합
/research-simple → /연구-통합

# 모두 동일하게 작동하되, 더 스마트하게!
```