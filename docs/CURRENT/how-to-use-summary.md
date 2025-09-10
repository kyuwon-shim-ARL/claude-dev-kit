# 📚 Research Project Manager 사용법 총정리

## 🎯 이렇게 사용하세요!

### 방법 1: Python 코드에서 직접 사용
```python
from research_project_manager import ResearchProjectManager

# 시작
manager = ResearchProjectManager()
manager.init_project("my_research", "나의 연구")
manager.track_progress("오늘 작업 완료")
```

### 방법 2: Claude Code와 대화로 사용
```
You: "신약 개발 연구 프로젝트를 시작해줘"
Claude: [프로젝트 생성 및 구조 설정]

You: "화합물 1000개 스크리닝 완료했어"
Claude: [진행사항 자동 기록]

You: "지금까지 결과 검증하는 스크립트 만들어줘"
Claude: [검증 스크립트 자동 생성]
```

### 방법 3: Jupyter Notebook에서 인터랙티브 사용
```python
# 셀 1: 초기화
from research_project_manager import ResearchProjectManager
manager = ResearchProjectManager()

# 셀 2: 프로젝트 생성
manager.init_project("biomarker_discovery", "바이오마커 발굴")

# 셀 3: 실시간 작업 기록
manager.track_progress("Sample 1-100 analyzed")
```

## 📁 생성되는 구조
```
research_projects/
└── 2025-09-10_my_research/
    ├── notebooks/      → Jupyter 노트북 저장
    ├── data/           → 원본 및 처리된 데이터
    ├── results/        → 분석 결과
    ├── figures/        → 그래프 및 이미지
    ├── docs/           → 프로젝트 문서
    ├── scripts/        → 실행 스크립트
    └── timeline.md     → 자동 생성되는 작업 기록
```

## 🚀 실제 워크플로우 예시

### 바이오인포매틱스 연구자의 하루
```python
# 아침: 프로젝트 시작
manager = ResearchProjectManager()
manager.init_project("genomics", "유전체 분석")

# 오전: 데이터 준비
manager.track_progress("FASTQ 파일 다운로드 완료", ["data/sample1.fastq"])
manager.explore_data("Quality control 시작")

# 점심 후: 분석 실행
manager.start_experiment("variant_calling", "변이 검출 파이프라인")
manager.track_progress("BWA alignment 완료")

# 오후: 결과 검증
manager.validate_results("통계적 유의성 검증")
manager.set_milestone("Phase 1 Complete", "초기 분석 완료")

# 저녁: 체크포인트 생성
manager.checkpoint("오늘 작업 완료, 내일 시각화 예정")
```

## 💡 핵심 명령어 11개

| 기능 | 명령어 | 언제 사용? |
|------|--------|-----------|
| **시작** | `init_project()` | 새 연구 시작할 때 |
| **기록** | `track_progress()` | 작업 완료할 때마다 |
| **목표** | `set_milestone()` | 큰 단계 완료 시 |
| **목록** | `list_projects()` | 전체 프로젝트 확인 |
| **전환** | `switch_project()` | 다른 프로젝트로 이동 |
| **보관** | `archive_project()` | 프로젝트 완료 시 |
| **탐색** | `explore_data()` | 데이터 분석 시작 |
| **가설** | `set_hypothesis()` | 연구 가설 설정 |
| **실험** | `start_experiment()` | 새 실험 시작 |
| **검증** | `validate_results()` | 결과 확인 |
| **저장** | `checkpoint()` | 중요 시점 백업 |

## 🔥 꿀팁

### 1. 어디서든 자동 감지
```python
# 프로젝트 깊은 폴더에서도 OK
os.chdir("research_projects/my_project/notebooks/deep/nested/")
manager = ResearchProjectManager()  # 자동으로 my_project 찾음!
```

### 2. 여러 프로젝트 동시 관리
```python
manager.switch_project("project_A")
# A 작업...
manager.switch_project("project_B")
# B 작업...
```

### 3. 한글 프로젝트명 지원
```python
manager.init_project("신약개발", "항암제 연구")
# → 2025-09-10_신약개발 생성됨
```

## 📖 자세한 문서

- **Quick Start**: [quick-start-research-manager.md](quick-start-research-manager.md)
- **전체 가이드**: [research-project-manager-usage-guide.md](research-project-manager-usage-guide.md)
- **예제 코드**: 
  - [simple_research_example.py](../../examples/simple_research_example.py)
  - [research_project_example.py](../../examples/research_project_example.py)

## ✅ 지금 바로 시작

```python
from research_project_manager import ResearchProjectManager
manager = ResearchProjectManager()
manager.init_project("test", "테스트 프로젝트")
print("🎉 시작했습니다!")
```

---

**한 줄 요약**: ResearchProjectManager로 연구 프로젝트를 체계적으로 관리하세요.

**핵심 장점**: 
- 📁 자동 디렉토리 구조 생성
- 📝 모든 작업 자동 기록
- 🔍 어디서든 프로젝트 자동 감지
- 🔒 보안 검증 내장

**시작 명령**: `from research_project_manager import ResearchProjectManager`