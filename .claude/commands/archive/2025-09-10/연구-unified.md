# /연구 - 통합 연구 관리 시스템 (Alias 지원)

## 사용법
```
/연구 [서브커맨드|별칭] [인자들]
```

## 🎯 서브커맨드 별칭 매핑

| 정식 명령어 | 별칭 (Alias) | 한글 | 설명 |
|------------|-------------|------|------|
| **init** | i, new | 시작, 초기화, 생성 | 새 프로젝트 시작 |
| **track** | t, log | 진행, 기록, 추적 | 진행사항 기록 |
| **experiment** | e, exp | 실험 | 실험 시작 |
| **hypothesis** | h, hyp | 가설 | 가설 설정 |
| **milestone** | m, mile | 마일스톤, 이정표 | 마일스톤 달성 |
| **checkpoint** | c, cp, save | 체크포인트, 저장 | 현재 상태 저장 |
| **status** | s, stat | 상태, 현황 | 프로젝트 상태 확인 |
| **list** | l, ls | 목록 | 프로젝트 목록 |
| **search** | f, find | 검색, 찾기 | 키워드 검색 |
| **backup** | b, bak | 백업 | 전체 백업 생성 |

## 실행 프로토콜

```bash
#!/bin/bash

# 서브커맨드 정규화 함수
normalize_subcommand() {
    case "$1" in
        # init 별칭들
        i|new|시작|초기화|생성)
            echo "init"
            ;;
        
        # track 별칭들
        t|log|진행|기록|추적)
            echo "track"
            ;;
        
        # experiment 별칭들
        e|exp|실험)
            echo "experiment"
            ;;
        
        # hypothesis 별칭들
        h|hyp|가설)
            echo "hypothesis"
            ;;
        
        # milestone 별칭들
        m|mile|마일스톤|이정표)
            echo "milestone"
            ;;
        
        # checkpoint 별칭들
        c|cp|save|체크포인트|저장)
            echo "checkpoint"
            ;;
        
        # status 별칭들
        s|stat|상태|현황)
            echo "status"
            ;;
        
        # list 별칭들
        l|ls|목록)
            echo "list"
            ;;
        
        # search 별칭들
        f|find|검색|찾기)
            echo "search"
            ;;
        
        # backup 별칭들
        b|bak|백업)
            echo "backup"
            ;;
        
        # 정식 명령어는 그대로 반환
        init|track|experiment|hypothesis|milestone|checkpoint|status|list|search|backup)
            echo "$1"
            ;;
        
        # 인식 불가능한 명령
        *)
            echo "unknown"
            ;;
    esac
}

# 메인 실행 로직
SUBCOMMAND=$(normalize_subcommand "$1")
shift  # 첫 번째 인자 제거

if [ "$SUBCOMMAND" = "unknown" ]; then
    echo "❌ 알 수 없는 서브커맨드입니다."
    echo ""
    echo "사용 가능한 명령어:"
    echo "  init (i, new, 시작)        - 새 프로젝트"
    echo "  track (t, log, 진행)       - 진행 기록"
    echo "  experiment (e, exp, 실험)  - 실험 시작"
    echo "  hypothesis (h, hyp, 가설)  - 가설 설정"
    echo "  milestone (m, 마일스톤)     - 마일스톤"
    echo "  checkpoint (c, cp, 저장)   - 체크포인트"
    echo "  status (s, 상태)           - 현황 확인"
    echo "  list (l, ls, 목록)         - 프로젝트 목록"
    echo "  search (f, find, 검색)     - 검색"
    echo "  backup (b, bak, 백업)      - 백업"
    exit 1
fi

# 정규화된 명령어로 실행
case "$SUBCOMMAND" in
    init)
        PROJECT_NAME="$1"
        PROJECT_DESC="$2"
        PROJECT_DIR="research_projects/$(date +%Y-%m-%d)_${PROJECT_NAME}"
        
        mkdir -p "${PROJECT_DIR}"/{notebooks,data,results,figures,docs,scripts,experiments}
        
        cat > "${PROJECT_DIR}/README.md" << EOF
# ${PROJECT_NAME}
Created: $(date '+%Y-%m-%d %H:%M')
Description: ${PROJECT_DESC}
EOF
        
        cat > "${PROJECT_DIR}/timeline.md" << EOF
# Research Timeline - ${PROJECT_NAME}
## Project Start: $(date '+%Y-%m-%d %H:%M')
---
EOF
        
        echo "✅ 프로젝트 생성: ${PROJECT_DIR}"
        ;;
    
    track)
        ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
        if [ -z "$ACTIVE_PROJECT" ]; then
            echo "❌ 활성 프로젝트가 없습니다. 먼저 프로젝트를 생성하세요."
            exit 1
        fi
        
        MESSAGE="$*"
        cat >> "${ACTIVE_PROJECT}/timeline.md" << EOF

## $(date '+%Y-%m-%d %H:%M')
**Note**: ${MESSAGE}

---
EOF
        
        echo "✅ 진행사항 기록: ${MESSAGE}"
        ;;
    
    experiment)
        ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
        EXP_NAME="$1"
        EXP_DESC="$2"
        EXP_DIR="${ACTIVE_PROJECT}/experiments/$(date +%Y%m%d_%H%M)_${EXP_NAME}"
        
        mkdir -p "${EXP_DIR}"
        cat > "${EXP_DIR}/README.md" << EOF
# Experiment: ${EXP_NAME}
- Started: $(date '+%Y-%m-%d %H:%M')
- Description: ${EXP_DESC}
- Status: Running

## Setup
[실험 설정]

## Results
[결과 기록]
EOF
        
        # 타임라인에도 기록
        cat >> "${ACTIVE_PROJECT}/timeline.md" << EOF

## $(date '+%Y-%m-%d %H:%M')
🧪 **Experiment Started**: ${EXP_NAME}
${EXP_DESC}

---
EOF
        
        echo "✅ 실험 시작: ${EXP_DIR}"
        ;;
    
    hypothesis)
        ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
        HYPOTHESIS="$*"
        
        # 가설 파일 생성 (없으면)
        if [ ! -f "${ACTIVE_PROJECT}/hypotheses.md" ]; then
            echo "# Hypotheses" > "${ACTIVE_PROJECT}/hypotheses.md"
        fi
        
        cat >> "${ACTIVE_PROJECT}/hypotheses.md" << EOF

## $(date '+%Y-%m-%d')
**Hypothesis**: ${HYPOTHESIS}
**Status**: Active
**Validation**: Pending
---
EOF
        
        # 타임라인에도 기록
        cat >> "${ACTIVE_PROJECT}/timeline.md" << EOF

## $(date '+%Y-%m-%d %H:%M')
💡 **Hypothesis**: ${HYPOTHESIS}

---
EOF
        
        echo "✅ 가설 설정: ${HYPOTHESIS}"
        ;;
    
    milestone)
        ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
        MILESTONE_NAME="$1"
        shift
        MILESTONE_DESC="$*"
        
        # 마일스톤 파일 생성 (없으면)
        if [ ! -f "${ACTIVE_PROJECT}/milestones.md" ]; then
            echo "# Milestones" > "${ACTIVE_PROJECT}/milestones.md"
        fi
        
        cat >> "${ACTIVE_PROJECT}/milestones.md" << EOF

## 🎯 $(date '+%Y-%m-%d'): ${MILESTONE_NAME}
${MILESTONE_DESC}
---
EOF
        
        # 타임라인에도 기록
        cat >> "${ACTIVE_PROJECT}/timeline.md" << EOF

## $(date '+%Y-%m-%d %H:%M')
🎯 **Milestone Achieved**: ${MILESTONE_NAME}
${MILESTONE_DESC}

---
EOF
        
        echo "✅ 마일스톤 달성: ${MILESTONE_NAME}"
        ;;
    
    checkpoint)
        ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
        CHECKPOINT_ID="$(date +%Y%m%d_%H%M%S)"
        CHECKPOINT_DIR="${ACTIVE_PROJECT}/checkpoints/${CHECKPOINT_ID}"
        MEMO="$*"
        
        # 체크포인트 디렉토리 생성
        mkdir -p "${CHECKPOINT_DIR}"
        
        # 현재 상태 백업
        cp "${ACTIVE_PROJECT}/timeline.md" "${CHECKPOINT_DIR}/" 2>/dev/null
        [ -f "${ACTIVE_PROJECT}/hypotheses.md" ] && cp "${ACTIVE_PROJECT}/hypotheses.md" "${CHECKPOINT_DIR}/"
        [ -f "${ACTIVE_PROJECT}/milestones.md" ] && cp "${ACTIVE_PROJECT}/milestones.md" "${CHECKPOINT_DIR}/"
        
        # 체크포인트 정보 저장
        cat > "${CHECKPOINT_DIR}/checkpoint.info" << EOF
ID=${CHECKPOINT_ID}
DATE=$(date '+%Y-%m-%d %H:%M:%S')
MEMO=${MEMO}
EOF
        
        # 타임라인에도 기록
        cat >> "${ACTIVE_PROJECT}/timeline.md" << EOF

## $(date '+%Y-%m-%d %H:%M')
⏸️ **Checkpoint Created**: ${CHECKPOINT_ID}
${MEMO}

---
EOF
        
        echo "✅ 체크포인트 생성: ${CHECKPOINT_ID}"
        [ -n "$MEMO" ] && echo "   메모: ${MEMO}"
        ;;
    
    status)
        echo "📊 연구 프로젝트 현황"
        echo "===================="
        
        for PROJECT_DIR in research_projects/*/; do
            if [ -d "$PROJECT_DIR" ]; then
                PROJECT_NAME=$(basename "$PROJECT_DIR")
                
                # 통계 계산
                TIMELINE_ENTRIES=$(grep -c "^##" "${PROJECT_DIR}/timeline.md" 2>/dev/null || echo 0)
                EXP_COUNT=$(ls -d "${PROJECT_DIR}"/experiments/* 2>/dev/null | wc -l)
                CHECKPOINT_COUNT=$(ls -d "${PROJECT_DIR}"/checkpoints/* 2>/dev/null | wc -l)
                
                echo ""
                echo "📁 ${PROJECT_NAME}"
                echo "   진행: ${TIMELINE_ENTRIES} 항목"
                echo "   실험: ${EXP_COUNT}개"
                echo "   체크포인트: ${CHECKPOINT_COUNT}개"
                
                # 최근 활동
                LAST_ENTRY=$(grep "^##" "${PROJECT_DIR}/timeline.md" 2>/dev/null | tail -1)
                if [ -n "$LAST_ENTRY" ]; then
                    echo "   최근: ${LAST_ENTRY#\#\# }"
                fi
            fi
        done
        ;;
    
    list)
        echo "📋 전체 프로젝트 목록"
        echo "==================="
        
        for PROJECT_DIR in research_projects/*/; do
            if [ -d "$PROJECT_DIR" ]; then
                PROJECT_NAME=$(basename "$PROJECT_DIR")
                FILE_COUNT=$(find "$PROJECT_DIR" -type f | wc -l)
                SIZE=$(du -sh "$PROJECT_DIR" | cut -f1)
                
                # README에서 설명 추출
                if [ -f "${PROJECT_DIR}/README.md" ]; then
                    DESC=$(grep "Description:" "${PROJECT_DIR}/README.md" | cut -d: -f2- | xargs)
                else
                    DESC="(설명 없음)"
                fi
                
                echo ""
                echo "• ${PROJECT_NAME}"
                echo "  설명: ${DESC}"
                echo "  파일: ${FILE_COUNT}개, 크기: ${SIZE}"
            fi
        done
        ;;
    
    search)
        SEARCH_TERM="$*"
        echo "🔍 '${SEARCH_TERM}' 검색 결과"
        echo "========================"
        
        # 모든 프로젝트에서 검색
        grep -r "${SEARCH_TERM}" research_projects/ --include="*.md" 2>/dev/null | \
            while IFS=: read -r file content; do
                PROJECT=$(echo "$file" | cut -d'/' -f2)
                FILE_NAME=$(basename "$file")
                echo ""
                echo "📁 ${PROJECT} / ${FILE_NAME}"
                echo "   ${content:0:100}..."
            done
        ;;
    
    backup)
        BACKUP_NAME="research_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
        tar -czf "${BACKUP_NAME}" research_projects/
        echo "✅ 백업 완료: ${BACKUP_NAME}"
        echo "   크기: $(du -h ${BACKUP_NAME} | cut -f1)"
        ;;
esac
```

## 🎯 사용 예시

### 짧은 별칭 사용
```bash
# 초단축 버전
/연구 i my_project              # init
/연구 t "오늘 진행사항"           # track
/연구 e baseline "첫 실험"        # experiment
/연구 h "가설 내용"              # hypothesis
/연구 m "마일스톤" "설명"         # milestone
/연구 c "체크포인트 메모"          # checkpoint
/연구 s                         # status
/연구 l                         # list
/연구 f "RGCCA"                 # search
/연구 b                         # backup
```

### 한글 사용
```bash
/연구 시작 프로젝트명 "설명"
/연구 진행 "오늘 한 일"
/연구 실험 exp01 "실험 설명"
/연구 가설 "이렇게 하면 될 것 같다"
/연구 마일스톤 "중요 달성" "상세 설명"
/연구 저장 "현재 상태 백업"
/연구 상태
/연구 목록
/연구 검색 "키워드"
/연구 백업
```

### 정식 명령어
```bash
/연구 init project_name "description"
/연구 track "progress note"
/연구 experiment exp_name "description"
/연구 hypothesis "hypothesis content"
/연구 milestone "name" "description"
/연구 checkpoint "memo"
/연구 status
/연구 list
/연구 search "keyword"
/연구 backup
```

## 📋 별칭 빠른 참조

```
초단축 (1글자):
  i → init      (새 프로젝트)
  t → track     (진행 기록)
  e → experiment (실험)
  h → hypothesis (가설)
  m → milestone  (마일스톤)
  c → checkpoint (체크포인트)
  s → status     (상태)
  l → list       (목록)
  f → search     (검색, find)
  b → backup     (백업)
```

## 🎯 핵심 장점

1. **유연성**: 영어, 한글, 단축어 모두 지원
2. **빠른 입력**: 1글자 별칭으로 빠른 기록
3. **학습 곡선 완화**: 익숙한 언어로 사용
4. **하위 호환**: 기존 명령어 모두 작동

## 💡 Pro Tips

```bash
# 가장 빠른 일일 워크플로우
/연구 t "아침 시작"              # track
/연구 e quick_test "빠른 테스트"  # experiment  
/연구 t "실험 결과: 성공"          # track
/연구 m "Phase 1" "완료"         # milestone
/연구 c "오늘 작업 완료"          # checkpoint

# 한 줄로 여러 작업
/연구 t "진행1" && /연구 t "진행2" && /연구 s
```