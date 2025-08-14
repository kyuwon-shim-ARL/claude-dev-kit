# 🎯 Claude Code Development Template

이 템플릿을 사용하여 새로운 레포에서도 **PaperFlow에서 사용한 효율적인 개발 방식**을 그대로 재현할 수 있습니다.

## ⚡ 30초 설정

### 방법 1: 원클릭 설치 (curl)

```bash
# 빈 프로젝트
mkdir my-new-project
cd my-new-project
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/install.sh | bash

# 기존 프로젝트
cd existing-project
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/install.sh | bash
```

### 방법 2: 수동 설치

```bash
# 1. 새 레포 생성 후 클론
git clone [your-new-repo-url]
cd [your-new-repo]

# 2. 이 템플릿 파일들 복사
# (이 파일들을 새 레포의 루트에 복사)

# 3. 자동 초기화 실행
./init-claude-repo.sh my_project_name "My project description"

# 4. 개발 시작
python scripts/test_setup.py
```

### 포함된 파일들:
- `CLAUDE.md` - 프로젝트 문서 템플릿
- `setup_claude_code_structure.py` - 디렉토리 구조 생성 스크립트  
- `init-claude-repo.sh` - 전체 자동 설정 스크립트
- `claude-code-best-practices.md` - 개발 방식 가이드

## 🔥 핵심 기능들

### ✅ 검증된 워크플로우
- **키워드 기반**: "기획", "구현", "안정화", "배포"
- **TodoWrite 중심**: 모든 복합 작업 추적
- **MECE 분석**: 정량적 진행률 측정  
- **세션 아카이브**: 재현 가능한 개발 기록

### ✅ 최적화된 구조
```
# 깔끔한 루트 - 필수 진입점만
├── main_app.py      # 메인 애플리케이션  
├── CLAUDE.md        # 프로젝트 문서
├── README.md        # 기본 설명
└── scripts/         # 개발 도구
    └── test_setup.py    # 시스템 검증

# 조직화된 구조
src/[project]/       # 핵심 구현체
core_features/       # 검증된 기능
docs/development/    # 세션 아카이브 + 가이드
tests/              # 모든 테스트
examples/           # 사용 예제
tools/              # 독립 유틸리티
archive/            # 정리된 레거시
```

### ✅ 자동화된 설정
- 디렉토리 구조 자동 생성
- 필수 파일들 템플릿 생성
- Git 초기화 및 첫 커밋
- 개발 가이드 자동 배치

## 🎯 사용법

### 개발 시작 패턴
```
# Claude Code에서 이렇게 말하면:
"기획해줘" → 탐색+분석+계획+PRD 순환 (수렴까지)
"구현해줘" → TodoWrite 계획 + 코딩 + 단위테스트
"안정화해줘" → 검증→문제발견→리팩토링→재검증 순환
"배포해줘" → 최종검증 + 구조화커밋 + 푸시
```

### 진행 상황 추적
```python
# TodoWrite 패턴
todos = [
    {"content": "기획: 요구사항 분석 + PRD 작성", "status": "completed"},
    {"content": "구현: 핵심 기능 + 단위테스트", "status": "in_progress"},
    {"content": "안정화: MECE 검증 + 품질확보", "status": "pending"},
    {"content": "배포: 최종검증 + 커밋&푸시", "status": "pending"}
]
```

### MECE 기반 보고
- ❌ "거의 다 됐어요" 
- ✅ "3/4 기능 완료, Neo4j 연결 1개 이슈 남음"

## 📚 추가 리소스

생성된 프로젝트에서 확인할 수 있는 가이드들:
- `docs/development/guides/claude-code-workflow.md`
- `docs/development/templates/session-template.md`
- `CLAUDE.md` (프로젝트별 맞춤 문서)

## 🚀 바로 시작하기

### 가장 빠른 방법 (curl)
```bash
# 단 한 줄로 설치 완료!
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/install.sh | bash
```

### 단계별 진행
1. **원클릭 설치**: 위 curl 명령 실행
2. **개발 시작**: `python scripts/test_setup.py` 후 "기획해줘"로 시작

### 수동 설치
1. **이 템플릿 다운로드**: 4개 핵심 파일 복사
2. **새 레포에서 실행**: `./init-claude-repo.sh project_name`
3. **개발 시작**: `python scripts/test_setup.py` 후 "기획해줘"로 시작

---

**이제 어떤 새로운 프로젝트에서도 PaperFlow에서 검증된 개발 방식을 바로 사용할 수 있습니다!**