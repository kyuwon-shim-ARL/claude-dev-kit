# /research-simple - 파일 기반 연구 관리 (Python 없음)

## 사용법
```
/research-simple [서브커맨드] [인자들]
```

## 실행 프로토콜

모든 작업을 **Bash 명령어와 파일 시스템**만으로 수행합니다.

### 1. 프로젝트 시작 (init)
```bash
# 프로젝트 디렉토리 생성
PROJECT_NAME="$2"
PROJECT_DIR="research_projects/$(date +%Y-%m-%d)_${PROJECT_NAME}"
mkdir -p "${PROJECT_DIR}"/{notebooks,data,results,figures,docs,scripts,experiments}

# 기본 파일 생성
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

# 메타데이터 (순수 텍스트)
cat > "${PROJECT_DIR}/.project_info" << EOF
NAME=${PROJECT_NAME}
CREATED=$(date +%Y-%m-%d)
STATUS=active
EXPERIMENTS=0
MILESTONES=0
EOF

echo "✅ 프로젝트 생성: ${PROJECT_DIR}"
```

### 2. 진행사항 기록 (track)
```bash
# 현재 활성 프로젝트 찾기
ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
if [ -z "$ACTIVE_PROJECT" ]; then
    echo "❌ 활성 프로젝트가 없습니다. 먼저 프로젝트를 생성하세요."
    exit 1
fi

# 타임라인에 기록
cat >> "${ACTIVE_PROJECT}/timeline.md" << EOF

## $(date '+%Y-%m-%d %H:%M')
$2
EOF

echo "✅ 진행사항 기록: $2"
```

### 3. 실험 시작 (experiment)
```bash
ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
EXP_NAME="$2"
EXP_DIR="${ACTIVE_PROJECT}/experiments/$(date +%Y%m%d_%H%M)_${EXP_NAME}"

mkdir -p "${EXP_DIR}"
cat > "${EXP_DIR}/README.md" << EOF
# Experiment: ${EXP_NAME}
- Started: $(date '+%Y-%m-%d %H:%M')
- Description: $3
- Status: Running

## Setup
[실험 설정 기록]

## Results
[결과 기록]
EOF

# 타임라인에도 기록
echo -e "\n## $(date '+%Y-%m-%d %H:%M')\n🧪 실험 시작: ${EXP_NAME}" >> "${ACTIVE_PROJECT}/timeline.md"

echo "✅ 실험 시작: ${EXP_DIR}"
```

### 4. 가설 설정 (hypothesis)
```bash
ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
HYPOTHESIS="$2"

# 가설 파일에 추가
cat >> "${ACTIVE_PROJECT}/hypotheses.md" << EOF

## $(date '+%Y-%m-%d')
**가설**: ${HYPOTHESIS}
**상태**: Active
**검증**: Pending
---
EOF

# 타임라인에도 기록
echo -e "\n## $(date '+%Y-%m-%d %H:%M')\n💡 가설: ${HYPOTHESIS}" >> "${ACTIVE_PROJECT}/timeline.md"

echo "✅ 가설 설정: ${HYPOTHESIS}"
```

### 5. 마일스톤 (milestone)
```bash
ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
MILESTONE_NAME="$2"
MILESTONE_DESC="$3"

# 마일스톤 파일에 추가
cat >> "${ACTIVE_PROJECT}/milestones.md" << EOF

## 🎯 $(date '+%Y-%m-%d'): ${MILESTONE_NAME}
${MILESTONE_DESC}
---
EOF

# 타임라인에도 기록
echo -e "\n## $(date '+%Y-%m-%d %H:%M')\n🎯 마일스톤: ${MILESTONE_NAME}" >> "${ACTIVE_PROJECT}/timeline.md"

# 메타데이터 업데이트 (bash로 카운트 증가)
if [ -f "${ACTIVE_PROJECT}/.project_info" ]; then
    . "${ACTIVE_PROJECT}/.project_info"
    MILESTONES=$((MILESTONES + 1))
    sed -i "s/MILESTONES=.*/MILESTONES=${MILESTONES}/" "${ACTIVE_PROJECT}/.project_info"
fi

echo "✅ 마일스톤 달성: ${MILESTONE_NAME}"
```

### 6. 체크포인트 (checkpoint)
```bash
ACTIVE_PROJECT=$(ls -td research_projects/*/ 2>/dev/null | head -1)
CHECKPOINT_ID="$(date +%Y%m%d_%H%M%S)"
CHECKPOINT_DIR="${ACTIVE_PROJECT}/checkpoints/${CHECKPOINT_ID}"
MEMO="$2"

# 현재 상태 백업
mkdir -p "${CHECKPOINT_DIR}"
cp "${ACTIVE_PROJECT}/timeline.md" "${CHECKPOINT_DIR}/"
cp "${ACTIVE_PROJECT}/.project_info" "${CHECKPOINT_DIR}/" 2>/dev/null

# 체크포인트 정보 저장
cat > "${CHECKPOINT_DIR}/checkpoint.info" << EOF
ID=${CHECKPOINT_ID}
DATE=$(date '+%Y-%m-%d %H:%M:%S')
MEMO=${MEMO}
EOF

echo "✅ 체크포인트 생성: ${CHECKPOINT_ID}"
```

### 7. 프로젝트 상태 (status)
```bash
echo "📊 연구 프로젝트 현황"
echo "===================="

for PROJECT_DIR in research_projects/*/; do
    if [ -d "$PROJECT_DIR" ]; then
        PROJECT_NAME=$(basename "$PROJECT_DIR")
        
        # 메타데이터 읽기
        if [ -f "${PROJECT_DIR}/.project_info" ]; then
            . "${PROJECT_DIR}/.project_info"
        fi
        
        # 통계 계산
        TIMELINE_ENTRIES=$(grep -c "^##" "${PROJECT_DIR}/timeline.md" 2>/dev/null || echo 0)
        EXP_COUNT=$(ls -d "${PROJECT_DIR}"/experiments/* 2>/dev/null | wc -l)
        
        echo ""
        echo "📁 ${PROJECT_NAME}"
        echo "   상태: ${STATUS:-active}"
        echo "   생성: ${CREATED:-unknown}"
        echo "   진행: ${TIMELINE_ENTRIES} 항목"
        echo "   실험: ${EXP_COUNT}개"
        echo "   마일스톤: ${MILESTONES:-0}개"
        
        # 최근 활동
        LAST_ENTRY=$(grep "^##" "${PROJECT_DIR}/timeline.md" 2>/dev/null | tail -1)
        if [ -n "$LAST_ENTRY" ]; then
            echo "   최근: ${LAST_ENTRY#\#\# }"
        fi
    fi
done
```

### 8. 프로젝트 목록 (list)
```bash
echo "📋 전체 프로젝트 목록"
echo "==================="

for PROJECT_DIR in research_projects/*/; do
    if [ -d "$PROJECT_DIR" ]; then
        PROJECT_NAME=$(basename "$PROJECT_DIR")
        FILE_COUNT=$(find "$PROJECT_DIR" -type f | wc -l)
        SIZE=$(du -sh "$PROJECT_DIR" | cut -f1)
        
        echo "- ${PROJECT_NAME} (파일: ${FILE_COUNT}, 크기: ${SIZE})"
    fi
done
```

### 9. 검색 (search)
```bash
SEARCH_TERM="$2"
echo "🔍 '${SEARCH_TERM}' 검색 결과"
echo "========================"

# 모든 프로젝트에서 검색
grep -r "${SEARCH_TERM}" research_projects/ --include="*.md" 2>/dev/null | \
    while IFS=: read -r file content; do
        PROJECT=$(echo "$file" | cut -d'/' -f2)
        FILE_NAME=$(basename "$file")
        echo "📁 ${PROJECT} / ${FILE_NAME}"
        echo "   ${content:0:100}..."
        echo ""
    done
```

### 10. 백업 (backup)
```bash
BACKUP_NAME="research_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "${BACKUP_NAME}" research_projects/
echo "✅ 백업 완료: ${BACKUP_NAME}"
echo "   크기: $(du -h ${BACKUP_NAME} | cut -f1)"
```

## 사용 예시

```bash
# 프로젝트 시작
/research-simple init drug_discovery "신약 개발 연구"

# 진행 기록
/research-simple track "ChEMBL 데이터베이스 다운로드 완료"

# 실험 시작
/research-simple experiment baseline_model "RDKit descriptors only"

# 가설 설정
/research-simple hypothesis "RGCCA가 예측 성능을 개선할 것"

# 마일스톤
/research-simple milestone "데이터 준비" "모든 데이터 전처리 완료"

# 체크포인트
/research-simple checkpoint "오늘 작업 완료, 내일 모델 학습"

# 상태 확인
/research-simple status

# 검색
/research-simple search "RGCCA"

# 백업
/research-simple backup
```

## 장점

1. **Python 불필요**: 순수 Bash와 파일 시스템만 사용
2. **투명성**: 모든 데이터가 읽기 쉬운 텍스트 파일
3. **이식성**: 어떤 Unix 시스템에서도 작동
4. **버전 관리**: Git과 완벽 호환
5. **간단함**: 복잡한 의존성 없음

## 파일 구조

```
research_projects/
├── 2025-09-10_drug_discovery/
│   ├── README.md           # 프로젝트 설명
│   ├── timeline.md          # 모든 활동 기록
│   ├── hypotheses.md        # 가설 목록
│   ├── milestones.md        # 마일스톤 기록
│   ├── .project_info        # 메타데이터
│   ├── notebooks/           # Jupyter 노트북
│   ├── data/               # 데이터 파일
│   ├── results/            # 결과 파일
│   ├── figures/            # 그래프, 이미지
│   ├── docs/               # 문서
│   ├── scripts/            # 스크립트
│   ├── experiments/        # 실험별 폴더
│   │   ├── 20250910_1430_baseline_model/
│   │   │   └── README.md
│   │   └── 20250910_1630_rgcca_v1/
│   │       └── README.md
│   └── checkpoints/        # 체크포인트
│       └── 20250910_143022/
│           ├── timeline.md
│           └── checkpoint.info
└── 2025-09-11_protein_analysis/
    └── ...
```

## 결론

**Python 스크립트 없이도 완전한 연구 관리 시스템 구현 가능!**

- 파일 시스템 = 데이터베이스
- Markdown = 문서화
- Bash = 로직
- 슬래시 커맨드 = 인터페이스