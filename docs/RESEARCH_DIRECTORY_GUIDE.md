# 📁 연구 디렉토리 관리 가이드

## 🎯 3가지 작업 모드

### 1️⃣ **프로젝트 루트 모드 (권장)**
```bash
# Claude 세션을 프로젝트 루트에서 시작
cd ~/projects/SMILES_property_webapp
claude

# 연구 작업 시 명시적 전환
/연구 switch "drug_toxicity"
/연구 track "작업 내용"
```

**장점:**
- 개발과 연구 모두 접근 가능
- 전체 프로젝트 컨텍스트 유지
- 도구 자동 링크 작동

### 2️⃣ **연구 디렉토리 모드**
```bash
# 특정 연구에 집중할 때
cd ~/projects/SMILES_property_webapp/research_projects/2025-09-09_drug_toxicity
claude

# 자동으로 해당 연구 감지
/연구 track "작업 내용"  # drug_toxicity에 자동 기록
```

**장점:**
- 해당 연구에만 집중
- 프로젝트 자동 감지
- 컨텍스트 최소화

### 3️⃣ **동적 전환 모드**
```bash
# 프로젝트 루트에서 시작
claude

# 필요시 디렉토리 이동
cd research_projects/2025-09-09_drug_toxicity
/연구 track "이 연구 작업"

# 다른 연구로 이동
cd ../2025-09-10_molecular_similarity
/연구 track "다른 연구 작업"

# 개발로 복귀
cd ../../src
/구현 "새 기능"
```

**장점:**
- 유연한 작업 전환
- 컨텍스트 동적 조정
- 실시간 포커스 변경

## 📊 모드별 사용 시나리오

| 시나리오 | 추천 모드 | 이유 |
|---------|----------|------|
| 새 연구 시작 | 프로젝트 루트 | 전체 구조 파악 필요 |
| 단일 연구 집중 | 연구 디렉토리 | 컨텍스트 최소화 |
| 연구-개발 병행 | 동적 전환 | 유연한 전환 필요 |
| 여러 연구 비교 | 프로젝트 루트 | 전체 관점 필요 |
| 긴 분석 작업 | 연구 디렉토리 | 집중력 유지 |

## 🤖 자동 감지 우선순위

```python
def detect_current_research():
    # 1순위: 현재 디렉토리
    cwd = os.getcwd()
    if "research_projects/" in cwd:
        return extract_project_from_path(cwd)
    
    # 2순위: 최근 활동
    if recent := get_recent_activity(5):
        return recent.project
    
    # 3순위: 메타데이터
    return metadata.get("active_project")
```

## 💡 실전 팁

### DO ✅
```bash
# 명확한 의도 표현
/연구 switch "drug_toxicity"  # 명시적 전환
/연구 status                  # 현재 상태 확인

# 작업 전 확인
pwd                           # 현재 위치 확인
/연구 list                    # 프로젝트 목록 확인
```

### DON'T ❌
```bash
# 애매한 작업
/연구 track "분석"            # 어느 프로젝트?

# 확인 없는 작업
cd ../../                     # 어디로 이동?
/연구 track "작업"            # 잘못된 프로젝트에 기록될 수 있음
```

## 🔧 환경 설정 (선택사항)

### .bashrc/.zshrc 설정
```bash
# 연구 프로젝트 빠른 이동
alias research='cd ~/projects/SMILES_property_webapp/research_projects'
alias drug='cd ~/projects/SMILES_property_webapp/research_projects/2025-09-09_drug_toxicity'

# 현재 연구 표시
function prompt_research() {
    if [[ $PWD == *"research_projects"* ]]; then
        echo " [🔬 $(basename $PWD)]"
    fi
}
PS1='${PS1}$(prompt_research)'
```

### VS Code 설정
```json
{
  "terminal.integrated.cwd": "${workspaceFolder}",
  "claude.defaultDirectory": "${workspaceFolder}",
  "files.exclude": {
    "**/research_projects/*/tools": true  // 심링크 숨기기
  }
}
```

## 📌 결론

**초보자**: 프로젝트 루트 모드 사용
**중급자**: 연구 디렉토리 모드로 집중
**고급자**: 동적 전환 모드로 유연하게

가장 중요한 것은 **일관성**입니다. 한 가지 모드를 선택하고 익숙해질 때까지 사용하세요.