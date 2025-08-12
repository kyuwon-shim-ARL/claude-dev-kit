# 🎯 Claude Code Development Template

이 템플릿을 사용하여 새로운 레포에서도 **PaperFlow에서 사용한 효율적인 개발 방식**을 그대로 재현할 수 있습니다.

## ⚡ 30초 설정

### 새 레포에서 사용하기:

```bash
# 1. 새 레포 생성 후 클론
git clone [your-new-repo-url]
cd [your-new-repo]

# 2. 이 템플릿 파일들 복사
# (이 파일들을 새 레포의 루트에 복사)

# 3. 자동 초기화 실행
./init-claude-repo.sh my_project_name "My project description"

# 4. 개발 시작
python test_setup.py
```

### 포함된 파일들:
- `CLAUDE.md` - 프로젝트 문서 템플릿
- `setup_claude_code_structure.py` - 디렉토리 구조 생성 스크립트  
- `init-claude-repo.sh` - 전체 자동 설정 스크립트
- `claude-code-best-practices.md` - 개발 방식 가이드

## 🔥 핵심 기능들

### ✅ 검증된 워크플로우
- **키워드 기반**: "분석", "시작", "정리", "검증", "커밋"
- **TodoWrite 중심**: 모든 복합 작업 추적
- **MECE 분석**: 정량적 진행률 측정  
- **세션 아카이브**: 재현 가능한 개발 기록

### ✅ 최적화된 구조
```
# 깔끔한 루트 - 필수 진입점만
├── main_app.py      # 메인 애플리케이션
├── test_setup.py    # 시스템 검증
├── CLAUDE.md        # 프로젝트 문서
└── README.md        # 기본 설명

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
"분석해줘" → 현황 파악 + 요구사항 정리
"시작해줘" → TodoWrite로 계획, 실행 개시
"정리해줘" → 리팩토링, 구조 개선
"검증해줘" → 테스트, 문서화
"커밋해줘" → 의미있는 커밋 생성
```

### 진행 상황 추적
```python
# TodoWrite 패턴
todos = [
    {"content": "분석: 현황 + 요구사항", "status": "completed"},
    {"content": "시작: 핵심 기능 구현", "status": "in_progress"},  
    {"content": "검증: 테스트 및 문서화", "status": "pending"}
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

1. **이 템플릿 다운로드**: 4개 핵심 파일 복사
2. **새 레포에서 실행**: `./init-claude-repo.sh project_name`
3. **개발 시작**: `python test_setup.py` 후 "분석해줘"로 시작

---

**이제 어떤 새로운 프로젝트에서도 PaperFlow에서 검증된 개발 방식을 바로 사용할 수 있습니다!**