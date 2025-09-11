# 🚀 Research Project Manager - Quick Start Guide

## 📌 한 줄 요약
**ResearchProjectManager**는 연구 프로젝트를 체계적으로 관리하는 Python 도구입니다.

## ⚡ 5분 안에 시작하기

### 1️⃣ 설치 및 Import
```python
# Python 스크립트나 Jupyter Notebook에서
from research_project_manager import ResearchProjectManager
```

### 2️⃣ 첫 번째 프로젝트 생성
```python
# Manager 초기화
manager = ResearchProjectManager()

# 프로젝트 생성
result = manager.init_project(
    name="my_research",
    description="나의 첫 연구 프로젝트"
)

print(f"✅ 프로젝트 생성 완료: {result['project_id']}")
```

### 3️⃣ 작업 기록하기
```python
# 진행사항 추적
manager.track_progress("데이터 100개 수집 완료")

# 마일스톤 설정
manager.set_milestone("데이터 수집 완료", "모든 데이터 준비됨")

# 실험 시작
manager.start_experiment("baseline", "기본 모델 테스트")
```

## 📊 실제 사용 예시

### 예시 1: 바이오인포매틱스 연구
```python
manager = ResearchProjectManager()

# 1. 유전체 분석 프로젝트 시작
manager.init_project("genomics", "유전체 변이 분석")

# 2. 데이터 탐색
manager.explore_data("FASTQ 파일 품질 확인")

# 3. 진행사항 기록
manager.track_progress("샘플 50개 시퀀싱 완료", 
                       ["data/sample_01.fastq"])

# 4. 가설 설정
manager.set_hypothesis("특정 변이가 질병과 연관됨")

# 5. 결과 검증
manager.validate_results("통계적 유의성 검증")
```

### 예시 2: 머신러닝 프로젝트
```python
manager = ResearchProjectManager()

# 1. ML 프로젝트 생성
manager.init_project("ml_prediction", "질병 예측 모델")

# 2. 여러 실험 수행
experiments = ["random_forest", "neural_network", "xgboost"]

for model in experiments:
    manager.start_experiment(model, f"{model} 모델 테스트")
    manager.track_progress(f"{model} 학습 완료")

# 3. 체크포인트 생성
manager.checkpoint("모든 모델 학습 완료")
```

## 🗂️ 생성되는 디렉토리 구조
```
research_projects/
└── 2025-09-09_my_research/
    ├── notebooks/      # Jupyter 노트북
    ├── data/           # 데이터 파일
    ├── results/        # 분석 결과
    ├── figures/        # 그래프/이미지
    ├── docs/           # 문서
    ├── scripts/        # 스크립트
    └── timeline.md     # 자동 생성 타임라인
```

## 💡 핵심 기능 11가지

| 명령어 | 설명 | 사용 예시 |
|--------|------|----------|
| `init_project` | 새 프로젝트 생성 | `manager.init_project("이름", "설명")` |
| `track_progress` | 진행사항 기록 | `manager.track_progress("작업 완료")` |
| `set_milestone` | 마일스톤 설정 | `manager.set_milestone("Phase 1", "완료")` |
| `list_projects` | 프로젝트 목록 | `manager.list_projects()` |
| `switch_project` | 프로젝트 전환 | `manager.switch_project("project_id")` |
| `archive_project` | 프로젝트 보관 | `manager.archive_project()` |
| `explore_data` | 데이터 탐색 | `manager.explore_data("EDA 시작")` |
| `set_hypothesis` | 가설 설정 | `manager.set_hypothesis("가설 내용")` |
| `start_experiment` | 실험 시작 | `manager.start_experiment("exp1", "설명")` |
| `validate_results` | 결과 검증 | `manager.validate_results("검증 내용")` |
| `checkpoint` | 체크포인트 | `manager.checkpoint("저장 지점")` |

## 🔍 디렉토리 자동 감지

프로젝트의 **어느 하위 디렉토리에서도** 자동으로 프로젝트를 인식합니다:

```python
# 깊은 하위 디렉토리에서도 작동
# 예: research_projects/my_project/notebooks/deep/nested/
manager = ResearchProjectManager()
# 자동으로 my_project를 찾아서 활성화!
```

## 🔒 보안 기능

- 위험한 문자 자동 제거 (`../`, `<>`, 등)
- 한글 프로젝트명 지원
- 파일시스템 공격 방지

## ❓ 자주 묻는 질문

**Q: 프로젝트를 어디서 찾을 수 있나요?**
```python
# 프로젝트 위치 확인
result = manager.init_project("test", "테스트")
print(f"위치: {result['path']}")
# 출력: 위치: research_projects/2025-09-09_test
```

**Q: 여러 프로젝트를 동시에 관리할 수 있나요?**
```python
# 프로젝트 전환
manager.switch_project("2025-09-09_project1")
# 작업...
manager.switch_project("2025-09-08_project2")
# 다른 작업...
```

**Q: 이전 작업을 복원할 수 있나요?**
```python
# 체크포인트 생성
checkpoint_id = manager.checkpoint("중요 시점")

# 나중에 복원
manager.resume_from_checkpoint(checkpoint_id)
```

## 🎯 Claude Code와 함께 사용

Claude Code 세션에서 자연어로 요청:

```
"신약 개발 연구 프로젝트를 시작해줘"
"진행사항을 기록해: 화합물 1000개 스크리닝 완료"
"실험 결과를 검증하는 스크립트를 만들어줘"
```

## 📚 더 알아보기

- [전체 사용 가이드](research-project-manager-usage-guide.md)
- [API 문서](../api/research_project_manager.md)
- [예제 코드](../../examples/research_project_example.py)

---

**시작하기**: `from research_project_manager import ResearchProjectManager`

**도움말**: `help(ResearchProjectManager)`

**버전**: 1.0.0 | **최종 업데이트**: 2025-09-09