# 🎯 슬래시 커맨드만으로 연구 관리하기

## 📌 핵심: 파일 기반 연구 관리 시스템

Python 스크립트 없이 **순수 파일 시스템과 슬래시 커맨드**만으로 연구를 관리하는 방법입니다.

## ✅ 슬래시 커맨드만으로 가능한 것

### 1. 프로젝트 구조 생성
```bash
# /연구시작 커맨드 (Claude가 실행)
mkdir -p research_projects/2025-09-10_my_research/{notebooks,data,results,figures,docs,scripts}
echo "# My Research Project" > research_projects/2025-09-10_my_research/README.md
echo "# Research Timeline" > research_projects/2025-09-10_my_research/timeline.md
```

### 2. 진행사항 기록 (파일 기반)
```bash
# /연구진행 커맨드
echo "## $(date '+%Y-%m-%d %H:%M')" >> timeline.md
echo "- 오늘 작업 내용" >> timeline.md
echo "---" >> timeline.md
```

### 3. 메타데이터 관리 (JSON 파일)
```bash
# /연구상태 커맨드
cat > project_status.json << EOF
{
  "name": "my_research",
  "status": "active",
  "created": "2025-09-10",
  "milestones": 3,
  "experiments": 5
}
EOF
```

### 4. 실험 폴더 생성
```bash
# /연구실험 커맨드
mkdir -p experiments/$(date +%Y%m%d)_experiment_name
echo "# Experiment: experiment_name" > experiments/$(date +%Y%m%d)_experiment_name/README.md
```

## 🔧 순수 슬래시 커맨드 구현

### /연구 슬래시 커맨드 (파일 시스템만 사용)

```markdown
<!--
file: .claude/commands/연구.md
-->

# /연구 - 파일 기반 연구 관리

## 실행 프로토콜

서브커맨드에 따라 다음 작업 수행:

### 시작 (init)
1. 디렉토리 구조 생성
2. README.md 생성
3. timeline.md 초기화
4. .research_meta.json 생성

### 진행 (track)
1. timeline.md에 타임스탬프 추가
2. 내용 기록
3. 관련 파일 링크 추가

### 실험 (experiment)
1. experiments/ 폴더에 새 디렉토리 생성
2. 실험 README.md 생성
3. timeline.md에 실험 시작 기록

### 상태 (status)
1. .research_meta.json 읽기
2. 최근 timeline.md 항목 표시
3. 실험 폴더 개수 카운트

## 구현 (Bash 명령어만 사용)

```bash
case "$subcommand" in
  "시작"|"init")
    mkdir -p research_projects/${project_name}/{notebooks,data,results,figures,docs,scripts}
    echo "# $project_name" > research_projects/${project_name}/README.md
    echo '{"name":"'$project_name'","created":"'$(date +%Y-%m-%d)'"}' > .research_meta.json
    ;;
    
  "진행"|"track")
    echo -e "\n## $(date '+%Y-%m-%d %H:%M')\n$message\n---" >> timeline.md
    ;;
    
  "실험"|"experiment")
    exp_dir="experiments/$(date +%Y%m%d)_${exp_name}"
    mkdir -p $exp_dir
    echo "# Experiment: $exp_name" > $exp_dir/README.md
    ;;
    
  "상태"|"status")
    cat .research_meta.json
    tail -20 timeline.md
    ls -d experiments/* | wc -l
    ;;
esac
```
```

## 📊 실제 사용 예시

### 연구 프로젝트 시작
```
You: "/연구 시작 drug_discovery"

Claude: 
[Bash 실행]
mkdir -p research_projects/2025-09-10_drug_discovery/{notebooks,data,results,figures,docs,scripts}
echo "# Drug Discovery Research" > research_projects/2025-09-10_drug_discovery/README.md
echo "# Research Timeline - Drug Discovery" > research_projects/2025-09-10_drug_discovery/timeline.md

✅ 프로젝트 생성 완료: research_projects/2025-09-10_drug_discovery/
```

### 진행사항 기록
```
You: "/연구 진행 ChEMBL 데이터 다운로드 완료"

Claude:
[Bash 실행]
echo -e "\n## $(date '+%Y-%m-%d %H:%M')" >> timeline.md
echo "- ChEMBL 데이터 다운로드 완료" >> timeline.md
echo "---" >> timeline.md

✅ 진행사항 기록됨
```

### 실험 시작
```
You: "/연구 실험 baseline_model"

Claude:
[Bash 실행]
mkdir -p experiments/20250910_baseline_model
echo "# Baseline Model Experiment" > experiments/20250910_baseline_model/README.md
echo "- Started: $(date)" >> experiments/20250910_baseline_model/README.md

✅ 실험 폴더 생성: experiments/20250910_baseline_model/
```

## 🎯 슬래시 커맨드만으로 가능한 기능

| 기능 | 구현 방법 | 파일/폴더 |
|------|----------|-----------|
| **프로젝트 생성** | `mkdir -p` | 폴더 구조 |
| **진행 기록** | `echo >>` | timeline.md |
| **실험 관리** | `mkdir` | experiments/ |
| **가설 기록** | `echo >>` | hypotheses.md |
| **마일스톤** | `echo >>` | milestones.md |
| **체크포인트** | `cp -r` | checkpoints/ |
| **상태 확인** | `cat`, `ls`, `wc` | 각종 파일 |
| **검색** | `grep`, `find` | 전체 파일 |
| **백업** | `tar`, `zip` | 압축 파일 |
| **공유** | `cp`, `rsync` | share/ |

## ❌ 슬래시 커맨드만으로 어려운 것

1. **복잡한 데이터 처리**
   - JSON 파싱/생성 (jq 필요)
   - 데이터 변환 및 계산
   - 관계형 데이터 관리

2. **동적 상태 관리**
   - 프로젝트 간 전환
   - 복잡한 메타데이터 업데이트
   - 트랜잭션 처리

3. **고급 검색/필터링**
   - 날짜 범위 검색
   - 복잡한 조건 필터링
   - 데이터 집계

## 💡 하이브리드 접근법

### 최소 Python 래퍼 (1개 파일만)
```python
#!/usr/bin/env python3
# research.py - 단독 실행 가능한 연구 관리 도구

import json
import sys
from pathlib import Path
from datetime import datetime

class SimpleResearchManager:
    def __init__(self):
        self.base = Path("research_projects")
        self.base.mkdir(exist_ok=True)
    
    def init_project(self, name, desc=""):
        project_dir = self.base / f"{datetime.now():%Y-%m-%d}_{name}"
        # ... 최소 구현
    
    # ... 핵심 기능만

if __name__ == "__main__":
    # 명령줄 인터페이스
    manager = SimpleResearchManager()
    # sys.argv 파싱
```

**사용자 레포와 분리:**
```bash
# ~/.local/bin/research 에 설치
cp research.py ~/.local/bin/research
chmod +x ~/.local/bin/research

# 어디서든 사용
research init my_project
research track "진행사항"
```

## 🎯 권장 전략

### 1. 순수 슬래시 커맨드 (80% 커버)
- 기본적인 연구 관리는 충분히 가능
- 파일 시스템 기반
- 외부 의존성 없음

### 2. 선택적 Python 도구 (20% 고급 기능)
- 사용자 홈 디렉토리에 설치
- 프로젝트와 분리
- 필요할 때만 사용

### 3. 웹 인터페이스 (선택사항)
- 간단한 HTML/JS 대시보드
- 파일 시스템 읽기 전용
- Python 없이도 작동

## 📋 실제 구현 예시

### 완전한 슬래시 커맨드 (Python 없음)

```bash
#!/bin/bash
# /연구 커맨드 구현

RESEARCH_BASE="research_projects"
CURRENT_PROJECT=""

case "$1" in
  init|시작)
    PROJECT_NAME="$2"
    PROJECT_DIR="$RESEARCH_BASE/$(date +%Y-%m-%d)_$PROJECT_NAME"
    mkdir -p "$PROJECT_DIR"/{notebooks,data,results,figures,docs,scripts}
    echo "# $PROJECT_NAME" > "$PROJECT_DIR/README.md"
    echo "# Timeline" > "$PROJECT_DIR/timeline.md"
    echo '{"name":"'$PROJECT_NAME'","created":"'$(date +%Y-%m-%d)'"}' > "$PROJECT_DIR/.meta.json"
    echo "✅ Created: $PROJECT_DIR"
    ;;
    
  track|진행)
    MESSAGE="$2"
    TIMELINE="$(find $RESEARCH_BASE -name timeline.md | head -1)"
    echo -e "\n## $(date '+%Y-%m-%d %H:%M')\n$MESSAGE\n---" >> "$TIMELINE"
    echo "✅ Tracked: $MESSAGE"
    ;;
    
  status|상태)
    for dir in $RESEARCH_BASE/*/; do
      if [ -f "$dir/.meta.json" ]; then
        echo "📁 $(basename $dir)"
        echo "   Files: $(find $dir -type f | wc -l)"
        echo "   Last: $(tail -1 $dir/timeline.md | head -1)"
      fi
    done
    ;;
esac
```

## 🎉 결론

**슬래시 커맨드만으로도 대부분의 연구 관리가 가능합니다!**

- ✅ 파일 시스템 기반 구조
- ✅ 텍스트 파일로 모든 기록
- ✅ Bash 명령어로 조작
- ✅ 사용자 레포에 Python 불필요
- ✅ 필요시 홈 디렉토리에 최소 도구만 설치

**핵심: 파일과 폴더가 곧 데이터베이스**